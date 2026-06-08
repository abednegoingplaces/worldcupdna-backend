from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.routers import matches, venues, predictions, leaderboard, profiles, auth, notifications, payments, admin, players
from app.database import engine
from app.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WorldCupDNA API",
    description="FIFA World Cup 2026 fan platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(matches.router)
app.include_router(venues.router)
app.include_router(predictions.router)
app.include_router(leaderboard.router)
app.include_router(profiles.router)
app.include_router(notifications.router)
app.include_router(payments.router)
app.include_router(admin.router)
app.include_router(players.router)

@app.get("/")
def root():
    return {
        "message": "WorldCupDNA API is live 🏆",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
