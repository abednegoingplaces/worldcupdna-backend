from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.models import Profile
from typing import Optional

router = APIRouter(prefix="/profiles", tags=["profiles"])

class ProfileCreate(BaseModel):
    id: str
    username: str
    favorite_team: str
    tactical_style: Optional[str] = None
    rival_hate_level: Optional[int] = 5

@router.get("/{user_id}")
def get_profile(user_id: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {
        "id": profile.id,
        "username": profile.username,
        "favorite_team": profile.favorite_team,
        "tactical_style": profile.tactical_style,
        "rival_hate_level": profile.rival_hate_level,
        "total_points": profile.total_points,
        "created_at": str(profile.created_at)
    }

@router.post("/")
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    existing = db.query(Profile).filter(Profile.id == profile.id).first()
    if existing:
        existing.username = profile.username
        existing.favorite_team = profile.favorite_team
        existing.tactical_style = profile.tactical_style
        existing.rival_hate_level = profile.rival_hate_level
        db.commit()
        db.refresh(existing)
        return {"profile": existing}

    new_profile = Profile(
        id=profile.id,
        username=profile.username,
        favorite_team=profile.favorite_team,
        tactical_style=profile.tactical_style,
        rival_hate_level=profile.rival_hate_level
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return {"profile": new_profile}