from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.venues import service
from app.modules.venues.schemas import VenueList, VenueOut, VenueSubmissionCreate

router = APIRouter(prefix="/venues", tags=["venues"])


@router.get("/", response_model=VenueList)
def get_venues(
    city: Optional[str] = None,
    county: Optional[str] = None,
    country: Optional[str] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius_km: float = 50,
    db: Session = Depends(get_db),
):
    venues = service.search(db, city, county, country, lat, lng, radius_km)
    return VenueList(venues=venues, total=len(venues))


@router.post("/submit", status_code=201)
def submit_venue(payload: VenueSubmissionCreate, db: Session = Depends(get_db)):
    submission = service.submit(db, payload)
    return {"id": submission.id, "status": submission.status}


@router.get("/{venue_id}", response_model=VenueOut)
def get_venue(venue_id: str, db: Session = Depends(get_db)):
    venue = service.get(db, venue_id)
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return venue
