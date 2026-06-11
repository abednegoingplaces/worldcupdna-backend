"""Match logic.

Source of truth for fixtures/results is football-data.org. We sync matches
into our ``matches`` table so predictions can reference them and so we can serve
the bulk of reads from our own DB (cheap, no rate limit). Standings are proxied
live (and cached) since they change as results come in.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.integrations.football_data import client as fd
from app.integrations.football_data.normalize import normalize_match
from app.modules.matches.models import Match

WC = settings.WORLD_CUP_COMPETITION_ID

# How often a read is allowed to trigger a fresh upstream sync. football-data
# moves matches SCHEDULED -> IN_PLAY -> FINISHED and only exposes updated scores
# when you re-poll, so without this the table freezes at its first-synced state
# (every match "scheduled", no results). The free tier allows 10 req/min and a
# sync is a single competition-wide request, so a short TTL is safe.
_SYNC_TTL = timedelta(seconds=90)
_last_sync: Optional[datetime] = None


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


# --- Syncing -----------------------------------------------------------------

def sync_world_cup(db: Session) -> int:
    """Pull every World Cup fixture from football-data and upsert into the DB.
    Returns the number of matches written."""
    raw_matches = fd.competition_matches(WC)
    count = 0
    for raw in raw_matches:
        data = normalize_match(raw)
        match_id = data["id"]
        existing = db.query(Match).filter(Match.id == match_id).first()
        fields = dict(
            external_id=data["external_id"],
            home_team=data["home_team"] or "TBD",
            home_team_code=data["home_team_code"],
            home_team_crest=data["home_team_crest"],
            away_team=data["away_team"] or "TBD",
            away_team_code=data["away_team_code"],
            away_team_crest=data["away_team_crest"],
            home_score=data["home_score"],
            away_score=data["away_score"],
            match_date=_parse_dt(data["match_date"]),
            stage=data["stage"],
            stage_code=data["stage_code"],
            group_name=data["group_name"],
            matchday=data["matchday"],
            status=data["status"],
            venue=data["venue"],
        )
        if existing:
            for k, v in fields.items():
                setattr(existing, k, v)
        else:
            db.add(Match(id=match_id, **fields))
        count += 1
    db.commit()
    return count


def ensure_synced(db: Session) -> None:
    """Keep the matches table fresh on read.

    Populates the table on first use (so the app works out of the box) and, once
    populated, re-syncs at most once per ``_SYNC_TTL`` so live scores and
    FINISHED results actually propagate from football-data instead of the table
    freezing at its first-synced state. A dedicated cron (``scripts.sync_matches``)
    can still be scheduled for tighter refresh during the tournament.
    """
    global _last_sync
    if not settings.FOOTBALL_API_KEY:
        return
    now = datetime.now(timezone.utc)
    is_empty = db.query(Match).count() == 0
    is_stale = _last_sync is None or (now - _last_sync) > _SYNC_TTL
    if not (is_empty or is_stale):
        return
    # Mark the attempt up front so concurrent requests don't all hit the upstream
    # within the same window; on failure we keep serving the cached DB rows.
    _last_sync = now
    try:
        sync_world_cup(db)
    except Exception:
        # Don't break reads if the upstream is unavailable.
        pass


# --- Reads -------------------------------------------------------------------

def list_matches(
    db: Session,
    stage: Optional[str] = None,
    status: Optional[str] = None,
    group: Optional[str] = None,
    matchday: Optional[int] = None,
) -> list[Match]:
    ensure_synced(db)
    query = db.query(Match)
    if stage:
        query = query.filter(Match.stage.ilike(f"%{stage}%"))
    if status:
        query = query.filter(Match.status == status)
    if group:
        query = query.filter(Match.group_name.ilike(f"%{group}%"))
    if matchday:
        query = query.filter(Match.matchday == matchday)
    return query.order_by(Match.match_date).all()


def _between(db: Session, start: datetime, end: datetime) -> list[Match]:
    return (
        db.query(Match)
        .filter(Match.match_date >= start, Match.match_date < end)
        .order_by(Match.match_date)
        .all()
    )


def today(db: Session) -> list[Match]:
    ensure_synced(db)
    now = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return _between(db, start, start + timedelta(days=1))


def recent(db: Session, days: int = 3) -> list[Match]:
    ensure_synced(db)
    now = datetime.now(timezone.utc)
    matches = (
        db.query(Match)
        .filter(
            Match.match_date >= now - timedelta(days=days),
            Match.match_date <= now,
            Match.status == "finished",
        )
        .order_by(Match.match_date.desc())
        .all()
    )
    return matches


def upcoming(db: Session, limit: int = 12) -> list[Match]:
    ensure_synced(db)
    now = datetime.now(timezone.utc)
    return (
        db.query(Match)
        .filter(Match.match_date >= now, Match.status == "scheduled")
        .order_by(Match.match_date)
        .limit(limit)
        .all()
    )


def live(db: Session) -> list[Match]:
    ensure_synced(db)
    return (
        db.query(Match)
        .filter(Match.status == "live")
        .order_by(Match.match_date)
        .all()
    )


def get(db: Session, match_id: str) -> Match:
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


def standings() -> list[dict]:
    """Live group standings from football-data, flattened to our shape."""
    groups = fd.standings(WC)
    result = []
    for g in groups:
        if g.get("type") and g["type"] != "TOTAL":
            continue
        table = []
        for row in g.get("table", []):
            team = row.get("team") or {}
            table.append(
                {
                    "position": row.get("position"),
                    "team": team.get("name"),
                    "team_code": team.get("tla"),
                    "crest": team.get("crest"),
                    "played": row.get("playedGames", 0),
                    "won": row.get("won", 0),
                    "draw": row.get("draw", 0),
                    "lost": row.get("lost", 0),
                    "goals_for": row.get("goalsFor", 0),
                    "goals_against": row.get("goalsAgainst", 0),
                    "goal_difference": row.get("goalDifference", 0),
                    "points": row.get("points", 0),
                }
            )
        result.append({"group": g.get("group"), "table": table})
    return result
