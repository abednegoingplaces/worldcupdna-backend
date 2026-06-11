from typing import Optional

from pydantic import BaseModel


class LeaderboardRow(BaseModel):
    rank: int
    user_id: str
    username: str
    avatar_url: Optional[str] = None
    favorite_team: Optional[str] = None
    total_points: int


class Leaderboard(BaseModel):
    rows: list[LeaderboardRow]
    total: int
    me: Optional[LeaderboardRow] = None
