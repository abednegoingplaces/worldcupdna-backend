from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base
from app.shared.ids import generate_uuid


class Match(Base):
    __tablename__ = "matches"

    # When synced from football-data.org this is the upstream match id (as str);
    # for manually-created matches it is a generated uuid.
    id = Column(String, primary_key=True, default=generate_uuid)
    external_id = Column(Integer, nullable=True, index=True)

    home_team = Column(String, nullable=False)
    home_team_code = Column(String, nullable=True)
    home_team_crest = Column(String, nullable=True)
    away_team = Column(String, nullable=False)
    away_team_code = Column(String, nullable=True)
    away_team_crest = Column(String, nullable=True)

    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)

    match_date = Column(DateTime(timezone=True), nullable=True, index=True)
    stage = Column(String, nullable=True)
    stage_code = Column(String, nullable=True)
    group_name = Column(String, nullable=True)
    matchday = Column(Integer, nullable=True)
    status = Column(String, default="scheduled", index=True)
    venue = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
