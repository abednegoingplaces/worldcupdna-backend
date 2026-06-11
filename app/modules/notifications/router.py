from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.notifications import service
from app.modules.notifications.schemas import NotificationList, NotificationOut
from app.modules.users.models import User

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/", response_model=NotificationList)
def list_notifications(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    notes = service.list_for_user(db, user.id)
    return NotificationList(notifications=notes, unread=service.unread_count(db, user.id))


@router.post("/{notification_id}/read", response_model=NotificationOut)
def mark_read(
    notification_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return service.mark_read(db, user.id, notification_id)


@router.post("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return {"marked_read": service.mark_all_read(db, user.id)}
