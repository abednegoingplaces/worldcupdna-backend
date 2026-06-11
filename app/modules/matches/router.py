from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.integrations.football_data.client import FootballDataError
from app.modules.matches import service
from app.modules.matches.schemas import GroupStanding, MatchList, MatchOut

router = APIRouter(prefix="/matches", tags=["matches"])


def _as_list(matches) -> MatchList:
    return MatchList(matches=matches, total=len(matches))


@router.get("/", response_model=MatchList)
def get_matches(
    stage: Optional[str] = None,
    status: Optional[str] = None,
    group: Optional[str] = None,
    matchday: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return _as_list(service.list_matches(db, stage, status, group, matchday))


@router.get("/today", response_model=MatchList)
def get_today(db: Session = Depends(get_db)):
    return _as_list(service.today(db))


@router.get("/recent", response_model=MatchList)
def get_recent(days: int = 3, db: Session = Depends(get_db)):
    return _as_list(service.recent(db, days))


@router.get("/upcoming", response_model=MatchList)
def get_upcoming(limit: int = 12, db: Session = Depends(get_db)):
    return _as_list(service.upcoming(db, limit))


@router.get("/live", response_model=MatchList)
def get_live(db: Session = Depends(get_db)):
    return _as_list(service.live(db))


@router.get("/standings", response_model=list[GroupStanding])
def get_standings():
    try:
        return service.standings()
    except FootballDataError as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@router.get("/{match_id}", response_model=MatchOut)
def get_match(match_id: str, db: Session = Depends(get_db)):
    return service.get(db, match_id)
