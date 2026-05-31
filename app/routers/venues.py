from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Venue

router = APIRouter(prefix="/venues", tags=["venues"])

@router.get("/")
def get_venues(db: Session = Depends(get_db)):
    venues = db.query(Venue).order_by(Venue.verified.desc()).all()
    return {"venues": [
        {
            "id": v.id,
            "name": v.name,
            "address": v.address,
            "area": v.area,
            "lat": v.lat,
            "lng": v.lng,
            "description": v.description,
            "verified": v.verified
        } for v in venues
    ]}