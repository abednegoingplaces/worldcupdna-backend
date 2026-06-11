from fastapi import APIRouter, HTTPException

from app.integrations.football_data.client import FootballDataError
from app.modules.players import service
from app.modules.players.schemas import ScorerList

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/scorers", response_model=ScorerList)
def top_scorers(limit: int = 20):
    try:
        scorers = service.top_scorers(limit)
    except FootballDataError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return ScorerList(scorers=scorers, total=len(scorers))


@router.get("/photo/{player_name}")
def player_photo(player_name: str):
    return service.player_photo(player_name)
