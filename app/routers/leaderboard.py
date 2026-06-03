from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import User

router = APIRouter(prefix="/api/v1/leaderboard", tags=["leaderboard"])

@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(User)\
        .order_by(User.total_points.desc())\
        .limit(50)\
        .all()
    return {"leaderboard": [
        {
            "id": u.id,
            "username": u.username,
            "favorite_team": u.favorite_team,
            "total_points": u.total_points
        } for u in users
    ]}