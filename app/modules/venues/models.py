from sqlalchemy import Boolean, Column, DateTime, Float, String
from sqlalchemy.sql import func

from app.core.database import Base
from app.shared.ids import generate_uuid


class Venue(Base):
    __tablename__ = "venues"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=True)
    county = Column(String, nullable=True)
    country = Column(String, default="Kenya")
    area = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class VenueSubmission(Base):
    __tablename__ = "venue_submissions"

    id = Column(String, primary_key=True, default=generate_uuid)
    submitted_by = Column(String, nullable=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    county = Column(String, nullable=True)
    country = Column(String, nullable=False)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
