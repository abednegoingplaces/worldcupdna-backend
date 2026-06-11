from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.modules.admin import service
from app.modules.admin.schemas import PlatformStats, ScoreUpdate
from app.modules.matches import service as matches_service
from app.modules.users.models import User

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)],
)


@router.patch("/matches/{match_id}/score")
def update_score(match_id: str, payload: ScoreUpdate, db: Session = Depends(get_db)):
    return service.set_score(db, match_id, payload.home_score, payload.away_score, payload.status)


@router.post("/matches/sync")
def sync_matches(db: Session = Depends(get_db)):
    count = matches_service.sync_world_cup(db)
    return {"synced": count}


@router.get("/stats", response_model=PlatformStats)
def platform_stats(db: Session = Depends(get_db)):
    return service.platform_stats(db)


@router.get("/users")
def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return service.list_users(db, skip, limit)


@router.patch("/users/{user_id}/deactivate")
def deactivate_user(user_id: str, db: Session = Depends(get_db)):
    return service.set_user_active(db, user_id, False)


@router.patch("/users/{user_id}/activate")
def activate_user(user_id: str, db: Session = Depends(get_db)):
    return service.set_user_active(db, user_id, True)


@router.get("/venues/pending")
def pending_venues(db: Session = Depends(get_db)):
    subs = service.pending_venues(db)
    return {"submissions": subs, "total": len(subs)}


@router.post("/venues/{submission_id}/approve")
def approve_venue(submission_id: str, db: Session = Depends(get_db)):
    return service.approve_venue(db, submission_id)


@router.post("/venues/{submission_id}/reject")
def reject_venue(submission_id: str, db: Session = Depends(get_db)):
    return service.reject_venue(db, submission_id)
