from app.database import engine, Base
from app.models.models import User, Match, Prediction, Venue
from dotenv import load_dotenv

load_dotenv()

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
