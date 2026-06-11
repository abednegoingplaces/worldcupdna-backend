from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base
from app.shared.ids import generate_uuid


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)

    # --- Football DNA profile ---
    favorite_team = Column(String, nullable=True)
    tactical_style = Column(String, nullable=True)
    rivalry_level = Column(Integer, default=5)

    # --- Game state ---
    total_points = Column(Integer, default=0, nullable=False)

    # --- Account flags ---
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)

    # --- Auth extras ---
    google_id = Column(String, nullable=True)
    verification_token = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
