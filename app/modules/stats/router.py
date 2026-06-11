from fastapi import APIRouter, HTTPException

from app.integrations.statsbomb.client import StatsBombError
from app.modules.stats import service
from app.modules.stats.schemas import CompetitionOut, ShotOut, StatsMatchOut

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/source")
def data_source():
    """Tells the frontend whether advanced data is live (paid) or historical (open)."""
    return {
        "provider": "statsbomb",
        "tier": "paid" if service.is_paid() else "open-data",
        "note": (
            "Live/current-season coverage"
            if service.is_paid()
            else "Free historical data (past tournaments, full xG)"
        ),
    }


@router.get("/competitions", response_model=list[CompetitionOut])
def competitions():
    try:
        return service.competitions()
    except StatsBombError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.get("/competitions/{competition_id}/seasons/{season_id}/matches", response_model=list[StatsMatchOut])
def matches(competition_id: int, season_id: int):
    try:
        return service.matches(competition_id, season_id)
    except StatsBombError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.get("/matches/{match_id}/shots", response_model=list[ShotOut])
def shot_map(match_id: int):
    try:
        return service.shot_map(match_id)
    except StatsBombError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
