"""User business logic — kept separate from HTTP concerns in the router."""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.users.models import User
from app.modules.users.schemas import InterestsUpdate, UserUpdate


def get_by_id(db: Session, user_id: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_by_username(db: Session, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_profile(db: Session, user: User, payload: UserUpdate) -> User:
    data = payload.model_dump(exclude_unset=True)

    new_username = data.get("username")
    if new_username and new_username != user.username:
        clash = (
            db.query(User)
            .filter(User.username == new_username, User.id != user.id)
            .first()
        )
        if clash:
            raise HTTPException(status_code=400, detail="Username already taken")

    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def update_interests(db: Session, user: User, payload: InterestsUpdate) -> User:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete_account(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


def search(db: Session, query: str, limit: int = 20) -> list[User]:
    return (
        db.query(User)
        .filter(User.username.ilike(f"%{query}%"))
        .order_by(User.total_points.desc())
        .limit(limit)
        .all()
    )
