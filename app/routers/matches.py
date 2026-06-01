from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Match
from typing import Optional

router = APIRouter(prefix="/api/v1/matches", tags=["matches"])

@router.get("/")
def get_matches(
    stage: Optional[str] = None,
    group: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Match).order_by(Match.match_date)
    if stage:
        query = query.filter(Match.stage == stage)
    if group:
        query = query.filter(Match.group_name == group)
    matches = query.all()
    return {"matches": [
        {
            "id": m.id,
            "home_team": m.home_team,
            "away_team": m.away_team,
            "home_score": m.home_score,
            "away_score": m.away_score,
            "match_date": str(m.match_date),
            "stage": m.stage,
            "group_name": m.group_name,
            "status": m.status
        } for m in matches
    ]}

@router.get("/{match_id}")
def get_match(match_id: str, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return {
        "id": match.id,
        "home_team": match.home_team,
        "away_team": match.away_team,
        "home_score": match.home_score,
        "away_score": match.away_score,
        "match_date": str(match.match_date),
        "stage": match.stage,
        "group_name": match.group_name,
        "status": match.status
    }