from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.notifications.models import Notification


def create(db: Session, user_id: str, title: str, message: str, type: str = "info") -> Notification:
    note = Notification(user_id=user_id, title=title, message=message, type=type)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def list_for_user(db: Session, user_id: str) -> list[Notification]:
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def unread_count(db: Session, user_id: str) -> int:
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id, Notification.read == False)  # noqa: E712
        .count()
    )


def mark_read(db: Session, user_id: str, notification_id: str) -> Notification:
    note = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == user_id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Notification not found")
    note.read = True
    db.commit()
    db.refresh(note)
    return note


def mark_all_read(db: Session, user_id: str) -> int:
    updated = (
        db.query(Notification)
        .filter(Notification.user_id == user_id, Notification.read == False)  # noqa: E712
        .update({Notification.read: True})
    )
    db.commit()
    return updated
