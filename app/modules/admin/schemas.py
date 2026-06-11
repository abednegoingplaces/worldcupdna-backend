from pydantic import BaseModel


class ScoreUpdate(BaseModel):
    home_score: int
    away_score: int
    status: str = "finished"


class PlatformStats(BaseModel):
    total_users: int
    total_predictions: int
    total_matches: int
    finished_matches: int
    live_matches: int
    upcoming_matches: int
