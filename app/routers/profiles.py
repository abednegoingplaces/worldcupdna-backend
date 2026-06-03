from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.models import User
from typing import Optional

router = APIRouter(prefix="/api/v1/users", tags=["users"])

class UserUpdate(BaseModel):
    username: Optional[str] = None
    favorite_team: Optional[str] = None
    tactical_style: Optional[str] = None
    rivalry_level: Optional[int] = None
    full_name: Optional[str] = None

class InterestsUpdate(BaseModel):
    favorite_team: Optional[str] = None
    tactical_style: Optional[str] = None
    rivalry_level: Optional[int] = None

@router.get("/me")
def get_my_profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "avatar_url": user.avatar_url,
        "favorite_team": user.favorite_team,
        "tactical_style": user.tactical_style,
        "rivalry_level": user.rivalry_level,
        "total_points": user.total_points,
        "is_verified": user.is_verified,
        "created_at": str(user.created_at)
    }

@router.patch("/me")
def update_my_profile(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.username:
        existing = db.query(User).filter(
            User.username == payload.username,
            User.id != user_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = payload.username
    if payload.favorite_team:
        user.favorite_team = payload.favorite_team
    if payload.tactical_style:
        user.tactical_style = payload.tactical_style
    if payload.rivalry_level is not None:
        user.rivalry_level = payload.rivalry_level
    if payload.full_name:
        user.full_name = payload.full_name

    db.commit()
    db.refresh(user)
    return {"message": "Profile updated successfully", "user": {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "favorite_team": user.favorite_team,
        "tactical_style": user.tactical_style,
        "rivalry_level": user.rivalry_level,
    }}

@router.delete("/me")
def delete_my_account(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "Account deleted successfully"}

@router.post("/me/avatar")
def upload_avatar(
    user_id: str,
    avatar_url: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.avatar_url = avatar_url
    db.commit()
    return {"message": "Avatar updated", "avatar_url": avatar_url}

@router.put("/me/interests")
def update_interests(
    user_id: str,
    payload: InterestsUpdate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.favorite_team:
        user.favorite_team = payload.favorite_team
    if payload.tactical_style:
        user.tactical_style = payload.tactical_style
    if payload.rivalry_level is not None:
        user.rivalry_level = payload.rivalry_level

    db.commit()
    return {"message": "Interests updated successfully"}

@router.get("/search")
def search_users(
    q: str,
    db: Session = Depends(get_db)
):
    users = db.query(User).filter(
        User.username.ilike(f"%{q}%")
    ).limit(20).all()
    return {"users": [
        {
            "id": u.id,
            "username": u.username,
            "favorite_team": u.favorite_team,
            "avatar_url": u.avatar_url,
            "total_points": u.total_points
        } for u in users
    ]}

@router.get("/{username}")
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "username": user.username,
        "favorite_team": user.favorite_team,
        "avatar_url": user.avatar_url,
        "total_points": user.total_points,
        "created_at": str(user.created_at)
    }