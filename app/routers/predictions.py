from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.models import Prediction, Match, User
from typing import Optional

router = APIRouter(prefix="/api/v1/predictions", tags=["predictions"])

class PredictionCreate(BaseModel):
    user_id: str
    match_id: str
    predicted_home: int
    predicted_away: int

class PredictionUpdate(BaseModel):
    predicted_home: int
    predicted_away: int

@router.get("/")
def get_predictions(user_id: str, db: Session = Depends(get_db)):
    predictions = db.query(Prediction)\
        .filter(Prediction.user_id == user_id)\
        .order_by(Prediction.created_at.desc())\
        .all()
    return {"predictions": [
        {
            "id": p.id,
            "user_id": p.user_id,
            "match_id": p.match_id,
            "predicted_home": p.predicted_home,
            "predicted_away": p.predicted_away,
            "points": p.points,
            "created_at": str(p.created_at)
        } for p in predictions
    ]}

@router.post("/")
def create_prediction(pred: PredictionCreate, db: Session = Depends(get_db)):
    # Check if match exists and is not finished
    match = db.query(Match).filter(Match.id == pred.match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status == "finished":
        raise HTTPException(status_code=400, detail="Cannot predict on a finished match")

    existing = db.query(Prediction).filter(
        Prediction.user_id == pred.user_id,
        Prediction.match_id == pred.match_id
    ).first()

    if existing:
        existing.predicted_home = pred.predicted_home
        existing.predicted_away = pred.predicted_away
        db.commit()
        db.refresh(existing)
        return {"message": "Prediction updated", "prediction": {
            "id": existing.id,
            "predicted_home": existing.predicted_home,
            "predicted_away": existing.predicted_away
        }}

    new_pred = Prediction(
        user_id=pred.user_id,
        match_id=pred.match_id,
        predicted_home=pred.predicted_home,
        predicted_away=pred.predicted_away
    )
    db.add(new_pred)
    db.commit()
    db.refresh(new_pred)
    return {"message": "Prediction created", "prediction": {
        "id": new_pred.id,
        "predicted_home": new_pred.predicted_home,
        "predicted_away": new_pred.predicted_away
    }}

@router.patch("/{prediction_id}")
def update_prediction(
    prediction_id: str,
    payload: PredictionUpdate,
    db: Session = Depends(get_db)
):
    prediction = db.query(Prediction)\
        .filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    # Check match is not finished
    match = db.query(Match)\
        .filter(Match.id == prediction.match_id).first()
    if match and match.status == "finished":
        raise HTTPException(status_code=400, detail="Cannot update prediction — match already finished")

    prediction.predicted_home = payload.predicted_home
    prediction.predicted_away = payload.predicted_away
    db.commit()
    return {"message": "Prediction updated successfully"}

@router.delete("/{prediction_id}")
def delete_prediction(prediction_id: str, db: Session = Depends(get_db)):
    prediction = db.query(Prediction)\
        .filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    # Check match is not finished
    match = db.query(Match)\
        .filter(Match.id == prediction.match_id).first()
    if match and match.status == "finished":
        raise HTTPException(status_code=400, detail="Cannot delete prediction — match already finished")

    db.delete(prediction)
    db.commit()
    return {"message": "Prediction deleted successfully"}

@router.post("/score/{match_id}")
def score_predictions(match_id: str, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.status != "finished":
        raise HTTPException(status_code=400, detail="Match not finished yet")

    predictions = db.query(Prediction)\
        .filter(Prediction.match_id == match_id).all()

    scored = 0
    for pred in predictions:
        points = 0
        if pred.predicted_home == match.home_score and \
           pred.predicted_away == match.away_score:
            points = 3
        else:
            predicted_result = (pred.predicted_home > pred.predicted_away) - \
                               (pred.predicted_home < pred.predicted_away)
            actual_result = (match.home_score > match.away_score) - \
                           (match.home_score < match.away_score)
            if predicted_result == actual_result:
                points = 1

        pred.points = points

        user = db.query(User).filter(User.id == pred.user_id).first()
        if user:
            user.total_points = (user.total_points or 0) + points

        scored += 1

    db.commit()
    return {"message": f"Scored {scored} predictions for match {match_id}"}