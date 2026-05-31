from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Profile

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    profiles = db.query(Profile)\
        .order_by(Profile.total_points.desc())\
        .limit(50)\
        .all()
    return {"leaderboard": [
        {
            "id": p.id,
            "username": p.username,
            "favorite_team": p.favorite_team,
            "total_points": p.total_points
        } for p in profiles
    ]}