from typing import Optional

from pydantic import BaseModel


class CompetitionOut(BaseModel):
    competition_id: int
    season_id: int
    competition_name: Optional[str] = None
    season_name: Optional[str] = None
    country_name: Optional[str] = None


class StatsMatchOut(BaseModel):
    match_id: int
    home_team: Optional[str] = None
    away_team: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    match_date: Optional[str] = None
    competition_stage: Optional[str] = None


class ShotOut(BaseModel):
    minute: Optional[int] = None
    second: Optional[int] = None
    team: Optional[str] = None
    player: Optional[str] = None
    xg: Optional[float] = None
    outcome: Optional[str] = None
    location: Optional[list[float]] = None
