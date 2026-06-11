"""Global leaderboard derived from each user's accumulated prediction points."""
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.users.models import User


def _row(rank: int, user: User) -> dict:
    return {
        "rank": rank,
        "user_id": user.id,
        "username": user.username,
        "avatar_url": user.avatar_url,
        "favorite_team": user.favorite_team,
        "total_points": user.total_points or 0,
    }


def global_board(db: Session, limit: int = 100) -> list[dict]:
    users = (
        db.query(User)
        .filter(User.is_active == True)  # noqa: E712
        .order_by(User.total_points.desc(), User.username.asc())
        .limit(limit)
        .all()
    )
    return [_row(i + 1, u) for i, u in enumerate(users)]


def rank_for(db: Session, user: User) -> dict:
    """Dense rank of a single user across the whole board."""
    points = user.total_points or 0
    higher = (
        db.query(func.count(User.id))
        .filter(User.is_active == True, User.total_points > points)  # noqa: E712
        .scalar()
    )
    return _row(int(higher) + 1, user)


def board_for(db: Session, me: Optional[User], limit: int = 100) -> dict:
    rows = global_board(db, limit)
    total = db.query(func.count(User.id)).filter(User.is_active == True).scalar()  # noqa: E712
    me_row = rank_for(db, me) if me else None
    return {"rows": rows, "total": int(total or 0), "me": me_row}
