"""Admin operations: settling matches, moderation, platform metrics."""
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.matches.models import Match
from app.modules.predictions import service as predictions_service
from app.modules.users.models import User
from app.modules.venues.models import Venue, VenueSubmission


def set_score(db: Session, match_id: str, home: int, away: int, status: str) -> dict:
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    match.home_score = home
    match.away_score = away
    match.status = status
    db.commit()

    scored = 0
    if status == "finished":
        scored = predictions_service.score_match(db, match_id)
    return {
        "match_id": match_id,
        "score": f"{home} - {away}",
        "status": status,
        "predictions_scored": scored,
    }


def platform_stats(db: Session) -> dict:
    total_matches = db.query(Match).count()
    finished = db.query(Match).filter(Match.status == "finished").count()
    live = db.query(Match).filter(Match.status == "live").count()
    from app.modules.predictions.models import Prediction

    return {
        "total_users": db.query(User).count(),
        "total_predictions": db.query(Prediction).count(),
        "total_matches": total_matches,
        "finished_matches": finished,
        "live_matches": live,
        "upcoming_matches": total_matches - finished - live,
    }


def list_users(db: Session, skip: int = 0, limit: int = 50) -> dict:
    users = db.query(User).offset(skip).limit(limit).all()
    return {
        "users": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "total_points": u.total_points,
                "is_active": u.is_active,
                "is_verified": u.is_verified,
                "is_admin": u.is_admin,
                "created_at": str(u.created_at),
            }
            for u in users
        ],
        "total": db.query(User).count(),
    }


def set_user_active(db: Session, user_id: str, active: bool) -> dict:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = active
    db.commit()
    return {"user_id": user_id, "is_active": active}


def pending_venues(db: Session) -> list[VenueSubmission]:
    return (
        db.query(VenueSubmission)
        .filter(VenueSubmission.status == "pending")
        .order_by(VenueSubmission.created_at.desc())
        .all()
    )


def approve_venue(db: Session, submission_id: str) -> dict:
    sub = db.query(VenueSubmission).filter(VenueSubmission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    venue = Venue(
        name=sub.name,
        address=sub.address,
        city=sub.city,
        county=sub.county,
        country=sub.country,
        lat=sub.lat,
        lng=sub.lng,
        description=sub.description,
        verified=True,
    )
    db.add(venue)
    sub.status = "approved"
    db.commit()
    db.refresh(venue)
    return {"venue_id": venue.id, "status": "approved"}


def reject_venue(db: Session, submission_id: str) -> dict:
    sub = db.query(VenueSubmission).filter(VenueSubmission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    sub.status = "rejected"
    db.commit()
    return {"submission_id": submission_id, "status": "rejected"}
