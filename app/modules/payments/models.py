from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func

from app.core.database import Base
from app.shared.ids import generate_uuid


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)
    plan = Column(String, default="premium")
    status = Column(String, default="active")  # active | cancelled | expired
    starts_at = Column(DateTime(timezone=True), server_default=func.now())
    ends_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
