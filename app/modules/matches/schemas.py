from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MatchOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    home_team: str
    home_team_code: Optional[str] = None
    home_team_crest: Optional[str] = None
    away_team: str
    away_team_code: Optional[str] = None
    away_team_crest: Optional[str] = None
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    match_date: Optional[datetime] = None
    stage: Optional[str] = None
    group_name: Optional[str] = None
    matchday: Optional[int] = None
    status: str = "scheduled"
    venue: Optional[str] = None


class MatchList(BaseModel):
    matches: list[MatchOut]
    total: int


class StandingRow(BaseModel):
    position: int
    team: str
    team_code: Optional[str] = None
    crest: Optional[str] = None
    played: int
    won: int
    draw: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int


class GroupStanding(BaseModel):
    group: Optional[str] = None
    table: list[StandingRow]
