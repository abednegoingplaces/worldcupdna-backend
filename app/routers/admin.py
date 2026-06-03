from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.models import Match, User, Prediction
from typing import Optional

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

class ScoreUpdate(BaseModel):
    home_score: int
    away_score: int
    status: str = "finished"

class MatchCreate(BaseModel):
    id: str
    home_team: str
    away_team: str
    match_date: str
    stage: str
    group_name: Optional[str] = None

@router.patch("/matches/{match_id}/score")
def update_match_score(
    match_id: str,
    payload: ScoreUpdate,
    db: Session = Depends(get_db)
):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    match.home_score = payload.home_score
    match.away_score = payload.away_score
    match.status = payload.status
    db.commit()

    # Auto score predictions if match finished
    if payload.status == "finished":
        predictions = db.query(Prediction)\
            .filter(Prediction.match_id == match_id).all()

        scored = 0
        for pred in predictions:
            points = 0
            if pred.home_score == payload.home_score and \
               pred.away_score == payload.away_score:
                points = 3
            else:
                pred_result = (pred.home_score > pred.away_score) - \
                              (pred.home_score < pred.away_score)
                actual_result = (payload.home_score > payload.away_score) - \
                                (payload.home_score < payload.away_score)
                if pred_result == actual_result:
                    points = 1

            pred.points = points

            user = db.query(User).filter(User.id == pred.user_id).first()
            if user:
                user.total_points = (user.total_points or 0) + points
            scored += 1

        db.commit()
        return {
            "message": f"Score updated and {scored} predictions scored",
            "match_id": match_id,
            "score": f"{payload.home_score} - {payload.away_score}"
        }

    return {
        "message": "Score updated",
        "match_id": match_id,
        "score": f"{payload.home_score} - {payload.away_score}"
    }

@router.get("/stats")
def get_platform_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_predictions = db.query(Prediction).count()
    total_matches = db.query(Match).count()
    finished_matches = db.query(Match)\
        .filter(Match.status == "finished").count()
    live_matches = db.query(Match)\
        .filter(Match.status == "live").count()

    return {
        "total_users": total_users,
        "total_predictions": total_predictions,
        "total_matches": total_matches,
        "finished_matches": finished_matches,
        "live_matches": live_matches,
        "upcoming_matches": total_matches - finished_matches - live_matches
    }

@router.get("/users")
def get_all_users(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return {"users": [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "total_points": u.total_points,
            "is_active": u.is_active,
            "is_verified": u.is_verified,
            "created_at": str(u.created_at)
        } for u in users
    ], "total": db.query(User).count()}

@router.patch("/users/{user_id}/deactivate")
def deactivate_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"message": f"User {user.username} deactivated"}

@router.post("/matches/sync")
def sync_matches():
    return {
        "message": "Match sync from football-data.org coming soon",
        "status": "pending"
    }