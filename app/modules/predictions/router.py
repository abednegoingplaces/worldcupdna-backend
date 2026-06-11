from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin, get_current_user
from app.modules.predictions import service
from app.modules.predictions.schemas import (
    PredictionCreate,
    PredictionList,
    PredictionOut,
    PredictionUpdate,
)
from app.modules.users.models import User

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("/me", response_model=PredictionList)
def my_predictions(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    preds = service.list_for_user(db, user.id)
    return PredictionList(predictions=preds, total=len(preds))


@router.post("/", response_model=PredictionOut, status_code=201)
def make_prediction(
    payload: PredictionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return service.upsert(db, user.id, payload)


@router.patch("/{prediction_id}", response_model=PredictionOut)
def update_prediction(
    prediction_id: str,
    payload: PredictionUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return service.update(db, prediction_id, user.id, payload)


@router.delete("/{prediction_id}", status_code=204)
def delete_prediction(
    prediction_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service.delete(db, prediction_id, user.id)


@router.post("/score/{match_id}")
def score_match(
    match_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """Admin: settle a finished match and award points to all predictors."""
    scored = service.score_match(db, match_id)
    return {"match_id": match_id, "predictions_scored": scored}
