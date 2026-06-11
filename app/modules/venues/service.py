"""Watch-party venue discovery (sports bars / fan zones)."""
import math
from typing import Optional

from sqlalchemy.orm import Session

from app.modules.venues.models import Venue, VenueSubmission
from app.modules.venues.schemas import VenueSubmissionCreate


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres."""
    radius = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    return radius * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def search(
    db: Session,
    city: Optional[str] = None,
    county: Optional[str] = None,
    country: Optional[str] = None,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius_km: float = 50,
) -> list[dict]:
    query = db.query(Venue).order_by(Venue.verified.desc())
    if city:
        query = query.filter(Venue.city.ilike(f"%{city}%"))
    if county:
        query = query.filter(Venue.county.ilike(f"%{county}%"))
    if country:
        query = query.filter(Venue.country.ilike(f"%{country}%"))

    result: list[dict] = []
    for v in query.all():
        data = {
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
            "distance_km": None,
        }
        if lat is not None and lng is not None and v.lat and v.lng:
            distance = haversine_km(lat, lng, v.lat, v.lng)
            if distance > radius_km:
                continue
            data["distance_km"] = round(distance, 2)
        result.append(data)

    if lat is not None and lng is not None:
        result.sort(key=lambda x: x["distance_km"] if x["distance_km"] is not None else 9999)
    return result


def get(db: Session, venue_id: str) -> Optional[Venue]:
    return db.query(Venue).filter(Venue.id == venue_id).first()


def submit(db: Session, payload: VenueSubmissionCreate) -> VenueSubmission:
    submission = VenueSubmission(**payload.model_dump(), status="pending")
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission
