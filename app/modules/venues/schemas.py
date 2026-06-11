from typing import Optional

from pydantic import BaseModel, ConfigDict


class VenueOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    address: str
    city: Optional[str] = None
    county: Optional[str] = None
    country: Optional[str] = None
    area: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    description: Optional[str] = None
    verified: bool = False
    distance_km: Optional[float] = None


class VenueList(BaseModel):
    venues: list[VenueOut]
    total: int


class VenueSubmissionCreate(BaseModel):
    submitted_by: Optional[str] = None
    name: str
    address: str
    city: str
    county: Optional[str] = None
    country: str = "Kenya"
    lat: Optional[float] = None
    lng: Optional[float] = None
    description: Optional[str] = None
    contact: Optional[str] = None
