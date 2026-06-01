import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())


class Venue(Base):
    __tablename__ = "venues"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String)
    county = Column(String)
    country = Column(String, default="Kenya")
    area = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    description = Column(String)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class VenueSubmission(Base):
    __tablename__ = "venue_submissions"

    id = Column(String, primary_key=True, default=generate_uuid)
    submitted_by = Column(String)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    county = Column(String)
    country = Column(String, nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    description = Column(String)
    contact = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Match(Base):
    __tablename__ = "matches"

    id = Column(String, primary_key=True, default=generate_uuid)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    match_date = Column(DateTime(timezone=True))
    venue = Column(String)
    group_name = Column(String)
    stage = Column(String, default="Group Stage")
    home_score = Column(Integer)
    away_score = Column(Integer)
    status = Column(String, default="upcoming")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    favorite_team = Column(String)
    tactical_style = Column(String)
    rivalry_level = Column(Integer, default=5)
    points = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False)
    match_id = Column(String, nullable=False)
    home_score = Column(Integer, nullable=False)
    away_score = Column(Integer, nullable=False)
    points_earned = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    type = Column(String, default="info")
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False)
    plan = Column(String, default="free")
    status = Column(String, default="active")
    stripe_customer_id = Column(String)
    stripe_subscription_id = Column(String)
    starts_at = Column(DateTime(timezone=True), server_default=func.now())
    ends_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())