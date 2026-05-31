from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import matches, venues, leaderboard, predictions, profiles

app = FastAPI(
    title="WorldCupDNA API",
    description="Backend API for WorldCupDNA — FIFA World Cup 2026 Fan Platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(matches.router)
app.include_router(venues.router)
app.include_router(leaderboard.router)
app.include_router(predictions.router)
app.include_router(profiles.router)

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