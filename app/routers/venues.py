from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from app.database import get_db
from app.models.models import Venue, VenueSubmission
from typing import Optional
import math

router = APIRouter(prefix="/api/v1/venues", tags=["venues"])

class VenueSubmissionCreate(BaseModel):
    submitted_by: Optional[str] = None
    name: str
    address: str
    city: str
    county: Optional[str] = None
    country: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    description: Optional[str] = None
    contact: Optional[str] = None

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two coordinates"""
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(d_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@router.get("/")
def get_venues(
    city: Optional[str] = None,
    county: Optional[str] = None,
    country: Optional[str] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius_km: Optional[float] = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Venue).order_by(Venue.verified.desc())

    if city:
        query = query.filter(Venue.city.ilike(f"%{city}%"))
    if county:
        query = query.filter(Venue.county.ilike(f"%{county}%"))
    if country:
        query = query.filter(Venue.country.ilike(f"%{country}%"))

    venues = query.all()

    result = []
    for v in venues:
        venue_data = {
            "id": v.id,
            "name": v.name,
            "address": v.address,
            "city": v.city,
            "county": v.county,
            "country": v.country,
            "area": v.area,
            "lat": v.lat,
            "lng": v.lng,
            "description": v.description,
            "verified": v.verified,
        }

        # Add distance if user location provided
        if lat and lng and v.lat and v.lng:
            distance = calculate_distance(lat, lng, v.lat, v.lng)
            if distance <= radius_km:
                venue_data["distance_km"] = round(distance, 2)
                result.append(venue_data)
        else:
            result.append(venue_data)

    # Sort by distance if location provided
    if lat and lng:
        result.sort(key=lambda x: x.get("distance_km", 9999))

    return {"venues": result, "total": len(result)}

@router.get("/{venue_id}")
def get_venue(venue_id: str, db: Session = Depends(get_db)):
    venue = db.query(Venue).filter(Venue.id == venue_id).first()
    if not venue:
        raise HTTPException(status_code=404, detail="Venue not found")
    return {
        "id": venue.id,
        "name": venue.name,
        "address": venue.address,
        "city": venue.city,
        "county": venue.county,
        "country": venue.country,
        "area": venue.area,
        "lat": venue.lat,
        "lng": venue.lng,
        "description": venue.description,
        "verified": venue.verified,
    }

@router.post("/submit")
def submit_venue(submission: VenueSubmissionCreate, db: Session = Depends(get_db)):
    """Anyone can submit a venue for review"""
    new_submission = VenueSubmission(
        submitted_by=submission.submitted_by,
        name=submission.name,
        address=submission.address,
        city=submission.city,
        county=submission.county,
        country=submission.country,
        lat=submission.lat,
        lng=submission.lng,
        description=submission.description,
        contact=submission.contact,
        status="pending"
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return {
        "message": "Venue submitted successfully! We'll review and add it soon.",
        "submission_id": new_submission.id
    }

@router.get("/submissions/pending")
def get_pending_submissions(db: Session = Depends(get_db)):
    """Admin — get all pending venue submissions"""
    submissions = db.query(VenueSubmission)\
        .filter(VenueSubmission.status == "pending")\
        .order_by(VenueSubmission.created_at.desc())\
        .all()
    return {"submissions": [
        {
            "id": s.id,
            "name": s.name,
            "address": s.address,
            "city": s.city,
            "county": s.county,
            "country": s.country,
            "description": s.description,
            "contact": s.contact,
            "submitted_by": s.submitted_by,
            "status": s.status,
            "created_at": str(s.created_at)
        } for s in submissions
    ]}

@router.patch("/submissions/{submission_id}/approve")
def approve_submission(submission_id: str, db: Session = Depends(get_db)):
    """Admin — approve a venue submission and add to venues"""
    submission = db.query(VenueSubmission)\
        .filter(VenueSubmission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Add to venues table
    new_venue = Venue(
        name=submission.name,
        address=submission.address,
        city=submission.city,
        county=submission.county,
        country=submission.country,
        lat=submission.lat,
        lng=submission.lng,
        description=submission.description,
        verified=True
    )
    db.add(new_venue)

    # Update submission status
    submission.status = "approved"
    db.commit()

    return {"message": f"Venue '{submission.name}' approved and added!"}

@router.patch("/submissions/{submission_id}/reject")
def reject_submission(submission_id: str, db: Session = Depends(get_db)):
    """Admin — reject a venue submission"""
    submission = db.query(VenueSubmission)\
        .filter(VenueSubmission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    submission.status = "rejected"
    db.commit()
    return {"message": "Submission rejected"}