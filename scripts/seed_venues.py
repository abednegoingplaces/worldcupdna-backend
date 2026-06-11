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
    dict(name="Sierra Brasserie", address="Yaya Centre, Kilimani, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Kilimani", lat=-1.2929, lng=36.7836, description="Craft-beer brasserie with wall-to-wall screens", verified=True),
    dict(name="Geco Cafe", address="Galana Road, Kilimani, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Kilimani", lat=-1.2916, lng=36.7872, description="Buzzing sports cafe popular for EPL & big games", verified=True),
    dict(name="Score Sports Bar", address="Adams Arcade, Ngong Road, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Kilimani", lat=-1.2990, lng=36.7760, description="Dedicated sports bar, every match on screen", verified=True),
    dict(name="Tap n Brew", address="Ngong Road, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Ngong Road", lat=-1.3010, lng=36.7700, description="Relaxed bar with big screens and a roaring crowd", verified=False),
    dict(name="J's Fresh Bar & Kitchen", address="Westlands, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Westlands", lat=-1.2654, lng=36.8030, description="Trendy spot with screens across two floors", verified=True),
    dict(name="Mercury Lounge (Westgate)", address="Westgate Mall, Westlands, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Westlands", lat=-1.2570, lng=36.8030, description="Lounge with large screens and a lively match-day crowd", verified=True),
    dict(name="Explorer Tavern", address="Parklands, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Parklands", lat=-1.2620, lng=36.8170, description="Big-screen tavern, packed for derbies", verified=False),
    dict(name="1824 Whisky Bar", address="Langata Road, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Langata", lat=-1.3360, lng=36.7560, description="Garden bar with giant screens for major matches", verified=True),
    dict(name="Pavement Sports Bar", address="Westlands, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Westlands", lat=-1.2675, lng=36.8045, description="Late-night sports bar showing every fixture", verified=False),
    dict(name="Tribeka", address="Tom Mboya Street, CBD, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="CBD", lat=-1.2840, lng=36.8270, description="CBD entertainment spot with screens for big games", verified=False),
    dict(name="Sippers Lounge", address="Kenyatta Avenue, CBD, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="CBD", lat=-1.2845, lng=36.8210, description="Central lounge, popular with after-work fans", verified=False),
    dict(name="Brew Bistro & Lounge (Ngong Road)", address="Ngong Road, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Ngong Road", lat=-1.3020, lng=36.7720, description="Microbrewery with screens and a big match-night crowd", verified=True),
    dict(name="The Hub Karen Foodcourt", address="The Hub, Karen, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Karen", lat=-1.3290, lng=36.7110, description="Open-air screens at the foodcourt for tournament games", verified=False),
    dict(name="Sportsman's Arms", address="Thika Road, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Thika Road", lat=-1.2190, lng=36.8890, description="Long-standing sports hotel with big-match screenings", verified=True),
    dict(name="Roast by Carnivore", address="Langata, Nairobi", city="Nairobi", county="Nairobi", country="Kenya", area="Langata", lat=-1.3320, lng=36.7660, description="Outdoor screens and grill, great for afternoon kickoffs", verified=True),
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
