"""StatsBomb integration.

Two tiers:

* **Open Data** (free, no auth) — historical competitions published by StatsBomb
  on GitHub. Rich event data including shots with xG, lineups and (for some
  matches) 360 freeze frames. This is what powers our "deep stats" features
  today. Note: it is HISTORICAL — it does NOT contain live FIFA World Cup 2026
  data, so we use it for past-tournament analysis and player/xG showcases.

* **Paid API** (``https://data.statsbomb.com``) — live, comprehensive coverage.
  Requires a subscription (username + password). We wire the client so that the
  moment ``STATSBOMB_USERNAME`` / ``STATSBOMB_PASSWORD`` are set, paid endpoints
  light up. Without credentials we transparently fall back to open data.

Open-data layout: {base}/competitions.json,
  {base}/matches/{competition_id}/{season_id}.json,
  {base}/events/{match_id}.json, {base}/lineups/{match_id}.json
"""
from typing import Optional

import httpx

from app.core import cache
from app.core.config import settings

_PAID_BASE = "https://data.statsbomb.com/api"


class StatsBombError(Exception):
    pass


def has_paid_access() -> bool:
    return bool(settings.STATSBOMB_USERNAME and settings.STATSBOMB_PASSWORD)


def _open_get(path: str, ttl: int = 3600) -> object:
    url = f"{settings.STATSBOMB_OPEN_DATA_BASE}/{path.lstrip('/')}"
    cache_key = f"sb:open:{path}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    try:
        with httpx.Client(timeout=20.0) as client:
            resp = client.get(url)
    except httpx.HTTPError as exc:
        raise StatsBombError(f"StatsBomb open-data request failed: {exc}") from exc
    if resp.status_code != 200:
        raise StatsBombError(f"StatsBomb open-data returned {resp.status_code}")
    data = resp.json()
    cache.set(cache_key, data, ttl)
    return data


def _paid_get(path: str, ttl: int = 120) -> object:
    auth = (settings.STATSBOMB_USERNAME, settings.STATSBOMB_PASSWORD)
    url = f"{_PAID_BASE}/{path.lstrip('/')}"
    cache_key = f"sb:paid:{path}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    try:
        with httpx.Client(timeout=20.0, auth=auth) as client:
            resp = client.get(url)
    except httpx.HTTPError as exc:
        raise StatsBombError(f"StatsBomb API request failed: {exc}") from exc
    if resp.status_code == 401:
        raise StatsBombError("StatsBomb credentials rejected")
    if resp.status_code != 200:
        raise StatsBombError(f"StatsBomb API returned {resp.status_code}")
    data = resp.json()
    cache.set(cache_key, data, ttl)
    return data


# --- Public surface (provider-agnostic) --------------------------------------

def list_competitions() -> object:
    """All competitions/seasons available to us."""
    if has_paid_access():
        return _paid_get("competitions")
    return _open_get("competitions.json")


def list_matches(competition_id: int, season_id: int) -> object:
    if has_paid_access():
        return _paid_get(f"competitions/{competition_id}/seasons/{season_id}/matches")
    return _open_get(f"matches/{competition_id}/{season_id}.json")


def match_events(match_id: int) -> object:
    if has_paid_access():
        return _paid_get(f"events/{match_id}")
    return _open_get(f"events/{match_id}.json")


def match_lineups(match_id: int) -> object:
    if has_paid_access():
        return _paid_get(f"lineups/{match_id}")
    return _open_get(f"lineups/{match_id}.json")


def shot_xg(match_id: int) -> list[dict]:
    """Distilled list of shots with xG for a match — a friendly, small payload
    derived from the full event feed."""
    events = match_events(match_id)
    shots = []
    if isinstance(events, list):
        for ev in events:
            if (ev.get("type") or {}).get("name") == "Shot":
                shot = ev.get("shot") or {}
                shots.append(
                    {
                        "minute": ev.get("minute"),
                        "team": (ev.get("team") or {}).get("name"),
                        "player": (ev.get("player") or {}).get("name"),
                        "xg": shot.get("statsbomb_xg"),
                        "outcome": (shot.get("outcome") or {}).get("name"),
                    }
                )
    return shots
