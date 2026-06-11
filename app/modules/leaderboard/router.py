from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_optional_user
from app.modules.leaderboard import service
from app.modules.leaderboard.schemas import Leaderboard
from app.modules.users.models import User

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/", response_model=Leaderboard)
def get_leaderboard(
    limit: int = 100,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    return service.board_for(db, user, limit)
