"""Client for football-data.org (v4).

Wraps the REST API with:
  * automatic ``X-Auth-Token`` header injection
  * a short-lived TTL cache (the free tier is 10 requests/minute)
  * graceful error handling — callers get a typed result, never an exception
    bubbling up to the request handler.

Docs: https://docs.football-data.org/general/v4/
"""
from typing import Any, Optional

import httpx

from app.core import cache
from app.core.config import settings


class FootballDataError(Exception):
    """Raised for non-recoverable upstream errors (surfaced as 502 by routers)."""


def _headers() -> dict[str, str]:
    return {"X-Auth-Token": settings.FOOTBALL_API_KEY}


def _get(path: str, params: Optional[dict] = None, ttl: Optional[int] = None) -> dict:
    """Perform a cached GET against the football-data API.

    ``path`` is relative to the API base, e.g. ``/competitions/2000/matches``.
    """
    if not settings.FOOTBALL_API_KEY:
        raise FootballDataError("FOOTBALL_API_KEY is not configured")

    ttl = settings.FOOTBALL_CACHE_TTL if ttl is None else ttl
    cache_key = f"fd:{path}:{sorted((params or {}).items())}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    url = f"{settings.FOOTBALL_API_BASE}{path}"
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.get(url, headers=_headers(), params=params)
    except httpx.HTTPError as exc:  # network / timeout
        raise FootballDataError(f"Upstream request failed: {exc}") from exc

    if resp.status_code == 429:
        raise FootballDataError("Rate limit exceeded — try again shortly")
    if resp.status_code != 200:
        raise FootballDataError(f"Upstream returned {resp.status_code}")

    data = resp.json()
    cache.set(cache_key, data, ttl)
    return data


# --- Competitions -------------------------------------------------------------

def list_competitions() -> dict:
    return _get("/competitions", ttl=3600)


def get_competition(competition_id: int) -> dict:
    return _get(f"/competitions/{competition_id}", ttl=3600)


# --- Matches ------------------------------------------------------------------

def competition_matches(
    competition_id: int,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    status: Optional[str] = None,
    stage: Optional[str] = None,
    group: Optional[str] = None,
    matchday: Optional[int] = None,
) -> list[dict]:
    params = {
        k: v
        for k, v in {
            "dateFrom": date_from,
            "dateTo": date_to,
            "status": status,
            "stage": stage,
            "group": group,
            "matchday": matchday,
        }.items()
        if v is not None
    }
    data = _get(f"/competitions/{competition_id}/matches", params=params)
    return data.get("matches", [])


def get_match(match_id: int) -> dict:
    return _get(f"/matches/{match_id}")


def standings(competition_id: int) -> list[dict]:
    data = _get(f"/competitions/{competition_id}/standings", ttl=300)
    return data.get("standings", [])


def scorers(competition_id: int, limit: int = 10) -> list[dict]:
    data = _get(
        f"/competitions/{competition_id}/scorers",
        params={"limit": limit},
        ttl=300,
    )
    return data.get("scorers", [])


def teams(competition_id: int) -> list[dict]:
    data = _get(f"/competitions/{competition_id}/teams", ttl=3600)
    return data.get("teams", [])


def get_team(team_id: int) -> dict:
    return _get(f"/teams/{team_id}", ttl=3600)


def team_matches(team_id: int, status: Optional[str] = None, limit: int = 10) -> list[dict]:
    params: dict[str, Any] = {"limit": limit}
    if status:
        params["status"] = status
    data = _get(f"/teams/{team_id}/matches", params=params)
    return data.get("matches", [])
