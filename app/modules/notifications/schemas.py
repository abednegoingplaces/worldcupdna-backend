from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    message: str
    type: str
    read: bool
    created_at: Optional[datetime] = None


class NotificationList(BaseModel):
    notifications: list[NotificationOut]
    unread: int
