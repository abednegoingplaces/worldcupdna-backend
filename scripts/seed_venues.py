"""Seed the watch-party venues (Nairobi sports bars & fan zones).

Run:  python -m scripts.seed_venues
Matches are NOT seeded here — they come live from football-data.org via
``scripts.sync_matches``.
"""
from app.core.database import Base, SessionLocal, engine
from app import models_registry  # noqa: F401
from app.modules.venues.models import Venue

VENUES = [
    dict(name="The Alchemist", address="Westlands, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Westlands", lat=-1.2667, lng=36.8028, description="Popular sports bar with multiple big screens", verified=True),
    dict(name="K1 Klubhouse", address="Karen, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Karen", lat=-1.3167, lng=36.7167, description="Upscale sports lounge with giant screens", verified=True),
    dict(name="Brew Bistro", address="Westlands, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Westlands", lat=-1.2633, lng=36.8014, description="Rooftop bar perfect for evening matches", verified=True),
    dict(name="The Local", address="Kilimani, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Kilimani", lat=-1.2833, lng=36.7833, description="Lively neighborhood bar for big games", verified=True),
    dict(name="Olepolos Country Club", address="Langata, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Langata", lat=-1.3500, lng=36.7333, description="Outdoor screens, perfect for afternoon kickoffs", verified=True),
    dict(name="Gipsy Bar", address="Lavington, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Lavington", lat=-1.2833, lng=36.7667, description="Electric when African teams play", verified=True),
    dict(name="Havana Bar", address="Westlands, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Westlands", lat=-1.2611, lng=36.8019, description="Cuban-themed bar with great screens", verified=True),
    dict(name="Club Signature", address="Hurlingham, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Hurlingham", lat=-1.2944, lng=36.7869, description="Multiple screens and affordable drinks", verified=False),
]


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        added = 0
        for data in VENUES:
            if not db.query(Venue).filter(Venue.name == data["name"]).first():
                db.add(Venue(**data))
                added += 1
        db.commit()
        print(f"✅ Seeded {added} new venues ({len(VENUES)} total in seed list)")
    finally:
        db.close()


if __name__ == "__main__":
    main()
