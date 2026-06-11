"""Translate football-data.org payloads into our own flat shapes.

Keeping normalisation in one place means the rest of the app never depends on
the upstream JSON structure — if we swap providers we only touch this file.
"""
from typing import Optional

# football-data status -> our internal status
_STATUS_MAP = {
    "SCHEDULED": "scheduled",
    "TIMED": "scheduled",
    "IN_PLAY": "live",
    "PAUSED": "live",
    "FINISHED": "finished",
    "SUSPENDED": "scheduled",
    "POSTPONED": "postponed",
    "CANCELLED": "cancelled",
    "AWARDED": "finished",
}


def normalize_status(raw: Optional[str]) -> str:
    return _STATUS_MAP.get((raw or "").upper(), "scheduled")


def normalize_match(m: dict) -> dict:
    """Flatten a football-data match into our match shape."""
    home = m.get("homeTeam") or {}
    away = m.get("awayTeam") or {}
    score = (m.get("score") or {}).get("fullTime") or {}
    group = m.get("group")
    return {
        "id": str(m.get("id")),
        "external_id": m.get("id"),
        "home_team": home.get("name"),
        "home_team_code": home.get("tla"),
        "home_team_crest": home.get("crest"),
        "away_team": away.get("name"),
        "away_team_code": away.get("tla"),
        "away_team_crest": away.get("crest"),
        "home_score": score.get("home"),
        "away_score": score.get("away"),
        "match_date": m.get("utcDate"),
        "stage": (m.get("stage") or "").replace("_", " ").title() or None,
        "stage_code": m.get("stage"),
        "group_name": group.replace("_", " ").title() if group else None,
        "matchday": m.get("matchday"),
        "status": normalize_status(m.get("status")),
        "venue": m.get("venue"),
    }
