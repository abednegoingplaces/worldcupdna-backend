from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.users import service
from app.modules.users.models import User
from app.modules.users.schemas import (
    InterestsUpdate,
    UserMe,
    UserPublic,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserMe)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserMe)
def update_my_profile(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.update_profile(db, current_user, payload)


@router.delete("/me")
def delete_my_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service.delete_account(db, current_user)
    return {"message": "Account deleted successfully"}


@router.put("/me/interests", response_model=UserMe)
def update_interests(
    payload: InterestsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.update_interests(db, current_user, payload)


@router.get("/search", response_model=list[UserPublic])
def search_users(q: str, db: Session = Depends(get_db)):
    return service.search(db, q)


@router.get("/{username}", response_model=UserPublic)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    return service.get_by_username(db, username)
