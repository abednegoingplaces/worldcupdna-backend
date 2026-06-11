from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PredictionCreate(BaseModel):
    match_id: str
    predicted_home: int
    predicted_away: int


class PredictionUpdate(BaseModel):
    predicted_home: int
    predicted_away: int


class PredictionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    match_id: str
    predicted_home: int
    predicted_away: int
    points: int
    scored: int
    created_at: Optional[datetime] = None


class PredictionList(BaseModel):
    predictions: list[PredictionOut]
    total: int
