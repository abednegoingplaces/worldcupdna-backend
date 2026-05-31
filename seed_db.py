from app.database import SessionLocal
from app.models.models import Match, Venue
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

db = SessionLocal()

matches = [
    # Group A
    Match(id='g_a1', home_team='Mexico', away_team='Argentina', match_date=datetime(2026,6,11,19,0), stage='group', group_name='A', status='scheduled'),
    Match(id='g_a2', home_team='Nigeria', away_team='South Africa', match_date=datetime(2026,6,12,15,0), stage='group', group_name='A', status='scheduled'),
    Match(id='g_a3', home_team='Argentina', away_team='Nigeria', match_date=datetime(2026,6,16,19,0), stage='group', group_name='A', status='scheduled'),
    Match(id='g_a4', home_team='South Africa', away_team='Mexico', match_date=datetime(2026,6,16,19,0), stage='group', group_name='A', status='scheduled'),
    Match(id='g_a5', home_team='Argentina', away_team='South Africa', match_date=datetime(2026,6,20,19,0), stage='group', group_name='A', status='scheduled'),
    Match(id='g_a6', home_team='Nigeria', away_team='Mexico', match_date=datetime(2026,6,20,19,0), stage='group', group_name='A', status='scheduled'),
    # Group B
    Match(id='g_b1', home_team='USA', away_team='Canada', match_date=datetime(2026,6,12,0,0), stage='group', group_name='B', status='scheduled'),
    Match(id='g_b2', home_team='Uruguay', away_team='Ecuador', match_date=datetime(2026,6,12,22,0), stage='group', group_name='B', status='scheduled'),
    Match(id='g_b3', home_team='USA', away_team='Uruguay', match_date=datetime(2026,6,17,19,0), stage='group', group_name='B', status='scheduled'),
    Match(id='g_b4', home_team='Canada', away_team='Ecuador', match_date=datetime(2026,6,17,19,0), stage='group', group_name='B', status='scheduled'),
    Match(id='g_b5', home_team='USA', away_team='Ecuador', match_date=datetime(2026,6,21,19,0), stage='group', group_name='B', status='scheduled'),
    Match(id='g_b6', home_team='Canada', away_team='Uruguay', match_date=datetime(2026,6,21,19,0), stage='group', group_name='B', status='scheduled'),
    # Group C
    Match(id='g_c1', home_team='Brazil', away_team='Germany', match_date=datetime(2026,6,12,19,0), stage='group', group_name='C', status='scheduled'),
    Match(id='g_c2', home_team='Colombia', away_team='Chile', match_date=datetime(2026,6,13,15,0), stage='group', group_name='C', status='scheduled'),
    Match(id='g_c3', home_team='Brazil', away_team='Colombia', match_date=datetime(2026,6,17,22,0), stage='group', group_name='C', status='scheduled'),
    Match(id='g_c4', home_team='Germany', away_team='Chile', match_date=datetime(2026,6,17,22,0), stage='group', group_name='C', status='scheduled'),
    Match(id='g_c5', home_team='Brazil', away_team='Chile', match_date=datetime(2026,6,21,22,0), stage='group', group_name='C', status='scheduled'),
    Match(id='g_c6', home_team='Germany', away_team='Colombia', match_date=datetime(2026,6,21,22,0), stage='group', group_name='C', status='scheduled'),
    # Group D
    Match(id='g_d1', home_team='France', away_team='England', match_date=datetime(2026,6,13,0,0), stage='group', group_name='D', status='scheduled'),
    Match(id='g_d2', home_team='Belgium', away_team='Denmark', match_date=datetime(2026,6,13,19,0), stage='group', group_name='D', status='scheduled'),
    Match(id='g_d3', home_team='France', away_team='Belgium', match_date=datetime(2026,6,18,19,0), stage='group', group_name='D', status='scheduled'),
    Match(id='g_d4', home_team='England', away_team='Denmark', match_date=datetime(2026,6,18,19,0), stage='group', group_name='D', status='scheduled'),
    Match(id='g_d5', home_team='France', away_team='Denmark', match_date=datetime(2026,6,22,19,0), stage='group', group_name='D', status='scheduled'),
    Match(id='g_d6', home_team='England', away_team='Belgium', match_date=datetime(2026,6,22,19,0), stage='group', group_name='D', status='scheduled'),
    # Group E
    Match(id='g_e1', home_team='Spain', away_team='Portugal', match_date=datetime(2026,6,13,19,0), stage='group', group_name='E', status='scheduled'),
    Match(id='g_e2', home_team='Italy', away_team='Turkey', match_date=datetime(2026,6,14,15,0), stage='group', group_name='E', status='scheduled'),
    Match(id='g_e3', home_team='Spain', away_team='Italy', match_date=datetime(2026,6,18,22,0), stage='group', group_name='E', status='scheduled'),
    Match(id='g_e4', home_team='Portugal', away_team='Turkey', match_date=datetime(2026,6,18,22,0), stage='group', group_name='E', status='scheduled'),
    Match(id='g_e5', home_team='Spain', away_team='Turkey', match_date=datetime(2026,6,22,22,0), stage='group', group_name='E', status='scheduled'),
    Match(id='g_e6', home_team='Portugal', away_team='Italy', match_date=datetime(2026,6,22,22,0), stage='group', group_name='E', status='scheduled'),
    # Group F
    Match(id='g_f1', home_team='Morocco', away_team='Senegal', match_date=datetime(2026,6,14,0,0), stage='group', group_name='F', status='scheduled'),
    Match(id='g_f2', home_team='Cameroon', away_team='Ghana', match_date=datetime(2026,6,14,19,0), stage='group', group_name='F', status='scheduled'),
    Match(id='g_f3', home_team='Morocco', away_team='Cameroon', match_date=datetime(2026,6,19,19,0), stage='group', group_name='F', status='scheduled'),
    Match(id='g_f4', home_team='Senegal', away_team='Ghana', match_date=datetime(2026,6,19,19,0), stage='group', group_name='F', status='scheduled'),
    Match(id='g_f5', home_team='Morocco', away_team='Ghana', match_date=datetime(2026,6,23,19,0), stage='group', group_name='F', status='scheduled'),
    Match(id='g_f6', home_team='Senegal', away_team='Cameroon', match_date=datetime(2026,6,23,19,0), stage='group', group_name='F', status='scheduled'),
    # Group G
    Match(id='g_g1', home_team='Netherlands', away_team='Croatia', match_date=datetime(2026,6,14,19,0), stage='group', group_name='G', status='scheduled'),
    Match(id='g_g2', home_team='Austria', away_team='Switzerland', match_date=datetime(2026,6,15,15,0), stage='group', group_name='G', status='scheduled'),
    Match(id='g_g3', home_team='Netherlands', away_team='Austria', match_date=datetime(2026,6,19,22,0), stage='group', group_name='G', status='scheduled'),
    Match(id='g_g4', home_team='Croatia', away_team='Switzerland', match_date=datetime(2026,6,19,22,0), stage='group', group_name='G', status='scheduled'),
    Match(id='g_g5', home_team='Netherlands', away_team='Switzerland', match_date=datetime(2026,6,23,22,0), stage='group', group_name='G', status='scheduled'),
    Match(id='g_g6', home_team='Croatia', away_team='Austria', match_date=datetime(2026,6,23,22,0), stage='group', group_name='G', status='scheduled'),
    # Group H
    Match(id='g_h1', home_team='Japan', away_team='South Korea', match_date=datetime(2026,6,15,0,0), stage='group', group_name='H', status='scheduled'),
    Match(id='g_h2', home_team='Australia', away_team='Saudi Arabia', match_date=datetime(2026,6,15,19,0), stage='group', group_name='H', status='scheduled'),
    Match(id='g_h3', home_team='Japan', away_team='Australia', match_date=datetime(2026,6,20,19,0), stage='group', group_name='H', status='scheduled'),
    Match(id='g_h4', home_team='South Korea', away_team='Saudi Arabia', match_date=datetime(2026,6,20,19,0), stage='group', group_name='H', status='scheduled'),
    Match(id='g_h5', home_team='Japan', away_team='Saudi Arabia', match_date=datetime(2026,6,24,19,0), stage='group', group_name='H', status='scheduled'),
    Match(id='g_h6', home_team='South Korea', away_team='Australia', match_date=datetime(2026,6,24,19,0), stage='group', group_name='H', status='scheduled'),
    # Round of 16
    Match(id='r16_1', home_team='TBD', away_team='TBD', match_date=datetime(2026,6,28,19,0), stage='round_of_16', status='scheduled'),
    Match(id='r16_2', home_team='TBD', away_team='TBD', match_date=datetime(2026,6,28,23,0), stage='round_of_16', status='scheduled'),
    Match(id='r16_3', home_team='TBD', away_team='TBD', match_date=datetime(2026,6,29,19,0), stage='round_of_16', status='scheduled'),
    Match(id='r16_4', home_team='TBD', away_team='TBD', match_date=datetime(2026,6,29,23,0), stage='round_of_16', status='scheduled'),
    Match(id='r16_5', home_team='TBD', away_team='TBD', match_date=datetime(2026,6,30,19,0), stage='round_of_16', status='scheduled'),
    Match(id='r16_6', home_team='TBD', away_team='TBD', match_date=datetime(2026,6,30,23,0), stage='round_of_16', status='scheduled'),
    Match(id='r16_7', home_team='TBD', away_team='TBD', match_date=datetime(2026,7,1,19,0), stage='round_of_16', status='scheduled'),
    Match(id='r16_8', home_team='TBD', away_team='TBD', match_date=datetime(2026,7,1,23,0), stage='round_of_16', status='scheduled'),
    # Quarter Finals
    Match(id='qf_1', home_team='TBD', away_team='TBD', match_date=datetime(2026,7,4,19,0), stage='quarter_final', status='scheduled'),
    Match(id='qf_2', home_team='TBD', away_team='TBD', match_date=datetime(2026,7,4,23,0), stage='quarter_final', status='scheduled'),
    Match(id='qf_3', home_team='TBD', away_team='TBD', match_date=datetime(2026,7,5,19,0), stage='quarter_final', status='scheduled'),
    Match(id='qf_4', home_team='TBD', away_team='TBD', match_date=datetime(2026,7,5,23,0), stage='quarter_final', status='scheduled'),
    # Semi Finals
    Match(id='sf_1', home_team='TBD', away_team='TBD', match_date=datetime(2026,7,9,19,0), stage='semi_final', status='scheduled'),
    Match(id='sf_2', home_team='TBD', away_team='TBD', match_date=datetime(2026,7,10,19,0), stage='semi_final', status='scheduled'),
    # Third Place
    Match(id='tp', home_team='TBD', away_team='TBD', match_date=datetime(2026,7,14,19,0), stage='third_place', status='scheduled'),
    # Final
    Match(id='final', home_team='TBD', away_team='TBD', match_date=datetime(2026,7,19,19,0), stage='final', status='scheduled'),
]

venues = [
    Venue(name='The Alchemist', address='Westlands, Nairobi', area='Westlands', lat=-1.2667, lng=36.8028, description='Popular sports bar with multiple big screens', verified=True),
    Venue(name='K1 Klubhouse', address='Karen, Nairobi', area='Karen', lat=-1.3167, lng=36.7167, description='Upscale sports lounge with giant screens', verified=True),
    Venue(name='Brew Bistro', address='Westlands, Nairobi', area='Westlands', lat=-1.2633, lng=36.8014, description='Rooftop bar perfect for evening matches', verified=True),
    Venue(name='The Local', address='Kilimani, Nairobi', area='Kilimani', lat=-1.2833, lng=36.7833, description='Lively neighborhood bar for big games', verified=True),
    Venue(name='Olepolos Country Club', address='Langata, Nairobi', area='Langata', lat=-1.3500, lng=36.7333, description='Outdoor screens, perfect for afternoon kickoffs', verified=True),
    Venue(name='Gipsy Bar', address='Lavington, Nairobi', area='Lavington', lat=-1.2833, lng=36.7667, description='Electric when African teams play', verified=True),
    Venue(name='Havana Bar', address='Westlands, Nairobi', area='Westlands', lat=-1.2611, lng=36.8019, description='Cuban-themed bar with great screens', verified=True),
    Venue(name='Club Signature', address='Hurlingham, Nairobi', area='Hurlingham', lat=-1.2944, lng=36.7869, description='Multiple screens and affordable drinks', verified=False),
]

try:
    print("Seeding matches...")
    for match in matches:
        existing = db.query(Match).filter(Match.id == match.id).first()
        if not existing:
            db.add(match)
    db.commit()
    print(f"✅ {len(matches)} matches seeded")

    print("Seeding venues...")
    for venue in venues:
        existing = db.query(Venue).filter(Venue.name == venue.name).first()
        if not existing:
            db.add(venue)
    db.commit()
    print(f"✅ {len(venues)} venues seeded")

    print("🎉 Database seeded successfully!")
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()