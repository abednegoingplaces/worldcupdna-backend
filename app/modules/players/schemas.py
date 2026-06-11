from typing import Optional

from pydantic import BaseModel


class ScorerOut(BaseModel):
    rank: int
    player: str
    player_id: Optional[int] = None
    team: Optional[str] = None
    team_crest: Optional[str] = None
    nationality: Optional[str] = None
    goals: int = 0
    assists: Optional[int] = None
    penalties: Optional[int] = None


class ScorerList(BaseModel):
    scorers: list[ScorerOut]
    total: int
