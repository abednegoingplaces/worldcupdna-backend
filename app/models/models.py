from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False)
    favorite_team = Column(String, nullable=False)
    tactical_style = Column(String)
    rival_hate_level = Column(Integer, default=5)
    dna_badge_url = Column(String)
    total_points = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    predictions = relationship("Prediction", back_populates="user")


class Match(Base):
    __tablename__ = "matches"

    id = Column(String, primary_key=True)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_score = Column(Integer)
    away_score = Column(Integer)
    match_date = Column(DateTime(timezone=True), nullable=False)
    stage = Column(String, nullable=False)
    group_name = Column(String)
    status = Column(String, default="scheduled")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    predictions = relationship("Prediction", back_populates="match")


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("profiles.id", ondelete="CASCADE"))
    match_id = Column(String, ForeignKey("matches.id", ondelete="CASCADE"))
    predicted_home = Column(Integer, nullable=False)
    predicted_away = Column(Integer, nullable=False)
    points_earned = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("user_id", "match_id"),)

    user = relationship("Profile", back_populates="predictions")
    match = relationship("Match", back_populates="predictions")


class Venue(Base):
    __tablename__ = "venues"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    area = Column(String, nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    description = Column(String)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())