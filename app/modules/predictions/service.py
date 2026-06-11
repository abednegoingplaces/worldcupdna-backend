"""Prediction logic and scoring.

Scoring rules:
  * exact scoreline  -> 3 points
  * correct outcome  -> 1 point
  * otherwise        -> 0 points
"""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.matches.models import Match
from app.modules.predictions.models import Prediction
from app.modules.predictions.schemas import PredictionCreate, PredictionUpdate
from app.modules.users.models import User


def _sign(a: int, b: int) -> int:
    return (a > b) - (a < b)


def points_for(pred: Prediction, home_score: int, away_score: int) -> int:
    if pred.predicted_home == home_score and pred.predicted_away == away_score:
        return 3
    if _sign(pred.predicted_home, pred.predicted_away) == _sign(home_score, away_score):
        return 1
    return 0


def list_for_user(db: Session, user_id: str) -> list[Prediction]:
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .all()
    )


def upsert(db: Session, user_id: str, payload: PredictionCreate) -> Prediction:
    match = db.query(Match).filter(Match.id == payload.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status in ("live", "finished"):
        raise HTTPException(
            status_code=400, detail="Predictions are locked once a match kicks off"
        )

    existing = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id, Prediction.match_id == payload.match_id)
        .first()
    )
    if existing:
        existing.predicted_home = payload.predicted_home
        existing.predicted_away = payload.predicted_away
        db.commit()
        db.refresh(existing)
        return existing

    pred = Prediction(
        user_id=user_id,
        match_id=payload.match_id,
        predicted_home=payload.predicted_home,
        predicted_away=payload.predicted_away,
    )
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred


def _owned(db: Session, prediction_id: str, user_id: str) -> Prediction:
    pred = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found")
    if pred.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not your prediction")
    return pred


def _assert_open(db: Session, pred: Prediction) -> None:
    match = db.query(Match).filter(Match.id == pred.match_id).first()
    if match and match.status in ("live", "finished"):
        raise HTTPException(
            status_code=400, detail="Match already started — prediction is locked"
        )


def update(db: Session, prediction_id: str, user_id: str, payload: PredictionUpdate):
    pred = _owned(db, prediction_id, user_id)
    _assert_open(db, pred)
    pred.predicted_home = payload.predicted_home
    pred.predicted_away = payload.predicted_away
    db.commit()
    db.refresh(pred)
    return pred


def delete(db: Session, prediction_id: str, user_id: str) -> None:
    pred = _owned(db, prediction_id, user_id)
    _assert_open(db, pred)
    db.delete(pred)
    db.commit()


def score_match(db: Session, match_id: str) -> int:
    """Score all (unscored) predictions for a finished match and award points.
    Idempotent — re-running won't double-count."""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status != "finished" or match.home_score is None or match.away_score is None:
        raise HTTPException(status_code=400, detail="Match is not finished")

    predictions = (
        db.query(Prediction)
        .filter(Prediction.match_id == match_id, Prediction.scored == 0)
        .all()
    )
    scored = 0
    for pred in predictions:
        pts = points_for(pred, match.home_score, match.away_score)
        pred.points = pts
        pred.scored = 1
        user = db.query(User).filter(User.id == pred.user_id).first()
        if user:
            user.total_points = (user.total_points or 0) + pts
        scored += 1
    db.commit()
    return scored
