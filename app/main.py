from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import venues, matches, predictions, leaderboard
from app.database import engine
from app.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WorldCupDNA API",
    version="1.0.0",
    description="Fan identity and prediction platform for FIFA World Cup 2026"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(venues.router)
app.include_router(matches.router)
app.include_router(predictions.router)
app.include_router(leaderboard.router)

@app.get("/")
def root():
    return {
        "platform": "WorldCupDNA",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "live"
    }