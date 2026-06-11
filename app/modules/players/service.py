"""Player data.

Top scorers come from football-data.org (free tier). Player headshots are
fetched from TheSportsDB (free, no key). Advanced metrics (xG, shot maps)
come from StatsBomb when configured — see ``app.integrations.statsbomb``.
"""
import httpx

from app.core import cache
from app.core.config import settings
from app.integrations.football_data import client as fd

WC = settings.WORLD_CUP_COMPETITION_ID
_SPORTSDB = "https://www.thesportsdb.com/api/v1/json/3/searchplayers.php"


def top_scorers(limit: int = 20) -> list[dict]:
    raw = fd.scorers(WC, limit=limit)
    result = []
    for i, s in enumerate(raw):
        player = s.get("player") or {}
        team = s.get("team") or {}
        result.append(
            {
                "rank": i + 1,
                "player": player.get("name"),
                "player_id": player.get("id"),
                "team": team.get("name"),
                "team_crest": team.get("crest"),
                "nationality": player.get("nationality"),
                "goals": s.get("goals") or 0,
                "assists": s.get("assists"),
                "penalties": s.get("penalties"),
            }
        )
    return result


def player_photo(player_name: str) -> dict:
    name = player_name.replace("_", " ")
    cache_key = f"player_photo:{name.lower()}"

    def _fetch():
        try:
            resp = httpx.get(_SPORTSDB, params={"p": name}, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                players = data.get("player") or []
                if players:
                    return {"photo": players[0].get("strThumb")}
        except Exception:
            pass
        return {"photo": None}

    return cache.get_or_set(cache_key, 86400, _fetch)
