from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.models import Notification
from typing import Optional

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])

class NotificationCreate(BaseModel):
    user_id: str
    title: str
    message: str
    type: Optional[str] = "info"

@router.get("/")
def get_notifications(user_id: str, db: Session = Depends(get_db)):
    notifications = db.query(Notification)\
        .filter(Notification.user_id == user_id)\
        .order_by(Notification.created_at.desc())\
        .all()
    return {"notifications": [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "type": n.type,
            "read": n.read,
            "created_at": str(n.created_at)
        } for n in notifications
    ], "unread_count": sum(1 for n in notifications if not n.read)}

@router.post("/")
def create_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db)
):
    notification = Notification(
        user_id=payload.user_id,
        title=payload.title,
        message=payload.message,
        type=payload.type
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return {"message": "Notification sent", "id": notification.id}

@router.patch("/{notification_id}/read")
def mark_as_read(notification_id: str, db: Session = Depends(get_db)):
    notification = db.query(Notification)\
        .filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    notification.read = True
    db.commit()
    return {"message": "Marked as read"}

@router.patch("/read-all")
def mark_all_as_read(user_id: str, db: Session = Depends(get_db)):
    db.query(Notification)\
        .filter(Notification.user_id == user_id)\
        .update({"read": True})
    db.commit()
    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}")
def delete_notification(notification_id: str, db: Session = Depends(get_db)):
    notification = db.query(Notification)\
        .filter(Notification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(notification)
    db.commit()
    return {"message": "Notification deleted"}