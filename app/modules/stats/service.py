"""Advanced football analytics via StatsBomb.

By default this reads StatsBomb **Open Data** (free, historical — includes past
World Cups with full event data and xG). If paid StatsBomb credentials are
configured, the same calls transparently use the paid API which carries live /
current-season coverage. See ``app.integrations.statsbomb``.
"""
from app.integrations.statsbomb import client as sb


def competitions() -> list[dict]:
    raw = sb.list_competitions()
    return [
        {
            "competition_id": c.get("competition_id"),
            "season_id": c.get("season_id"),
            "competition_name": c.get("competition_name"),
            "season_name": c.get("season_name"),
            "country_name": c.get("country_name"),
        }
        for c in (raw or [])
    ]


def matches(competition_id: int, season_id: int) -> list[dict]:
    raw = sb.list_matches(competition_id, season_id)
    result = []
    for m in raw or []:
        home = m.get("home_team") or {}
        away = m.get("away_team") or {}
        result.append(
            {
                "match_id": m.get("match_id"),
                "home_team": home.get("home_team_name") if isinstance(home, dict) else home,
                "away_team": away.get("away_team_name") if isinstance(away, dict) else away,
                "home_score": m.get("home_score"),
                "away_score": m.get("away_score"),
                "match_date": m.get("match_date"),
                "competition_stage": (m.get("competition_stage") or {}).get("name")
                if isinstance(m.get("competition_stage"), dict)
                else m.get("competition_stage"),
            }
        )
    return result


def shot_map(match_id: int) -> list[dict]:
    return sb.shot_xg(match_id)


def is_paid() -> bool:
    return sb.has_paid_access()
