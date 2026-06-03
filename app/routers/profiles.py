from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.models import User
from typing import Optional

router = APIRouter(prefix="/api/v1/users", tags=["users"])

class UserCreate(BaseModel):
    id: str
    username: str
    favorite_team: str
    tactical_style: Optional[str] = None
    rival_hate_level: Optional[int] = 5

@router.get("/{user_id}")
def get_User(user_id: str, db: Session = Depends(get_db)):
    User = db.query(User).filter(User.id == user_id).first()
    if not User:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": User.id,
        "username": User.username,
        "favorite_team": User.favorite_team,
        "tactical_style": User.tactical_style,
        "rival_hate_level": User.rival_hate_level,
        "total_points": User.total_points,
        "created_at": str(User.created_at)
    }

@router.post("/")
def create_User(User: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.id == User.id).first()
    if existing:
        existing.username = User.username
        existing.favorite_team = User.favorite_team
        existing.tactical_style = User.tactical_style
        existing.rival_hate_level = User.rival_hate_level
        db.commit()
        db.refresh(existing)
        return {"User": existing}

    new_User = User(
        id=User.id,
        username=User.username,
        favorite_team=User.favorite_team,
        tactical_style=User.tactical_style,
        rival_hate_level=User.rival_hate_level
    )
    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return {"User": new_User}
