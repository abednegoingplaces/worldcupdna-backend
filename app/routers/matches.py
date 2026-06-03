from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Match
from typing import Optional
import httpx
import os

router = APIRouter(prefix="/api/v1/matches", tags=["matches"])

FOOTBALL_API_KEY = os.getenv("FOOTBALL_API_KEY")
FOOTBALL_API_BASE = "https://api.football-data.org/v4"
WC_2026_ID = 2000

def get_headers():
    return {"X-Auth-Token": FOOTBALL_API_KEY}

@router.get("/")
def get_matches(
    stage: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Match)
    if stage:
        query = query.filter(Match.stage.ilike(f"%{stage}%"))
    if status:
        query = query.filter(Match.status == status)
    matches = query.order_by(Match.match_date).all()
    return {"matches": [
        {
            "id": m.id,
            "home_team": m.home_team,
            "away_team": m.away_team,
            "match_date": str(m.match_date),
            "stage": m.stage,
            "group_name": m.group_name,
            "home_score": m.home_score,
            "away_score": m.away_score,
            "status": m.status,
            "venue": m.venue
        } for m in matches
    ], "total": len(matches)}

@router.get("/live")
async def get_live_matches():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{FOOTBALL_API_BASE}/competitions/{WC_2026_ID}/matches",
                headers=get_headers(),
                params={"status": "LIVE"},
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                return {"live_matches": data.get("matches", []), "source": "football-data.org"}
            else:
                return {"live_matches": [], "error": f"API returned {response.status_code}"}
        except Exception as e:
            return {"live_matches": [], "error": str(e)}

@router.get("/upcoming")
async def get_upcoming_matches():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{FOOTBALL_API_BASE}/competitions/{WC_2026_ID}/matches",
                headers=get_headers(),
                params={"status": "SCHEDULED"},
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                matches = data.get("matches", [])[:10]
                return {"upcoming_matches": matches, "source": "football-data.org"}
            else:
                return {"upcoming_matches": [], "error": f"API returned {response.status_code}"}
        except Exception as e:
            return {"upcoming_matches": [], "error": str(e)}

@router.get("/standings")
async def get_standings():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{FOOTBALL_API_BASE}/competitions/{WC_2026_ID}/standings",
                headers=get_headers(),
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"standings": [], "error": f"API returned {response.status_code}"}
        except Exception as e:
            return {"standings": [], "error": str(e)}

@router.get("/{match_id}")
def get_match(match_id: str, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return {
        "id": match.id,
        "home_team": match.home_team,
        "away_team": match.away_team,
        "match_date": str(match.match_date),
        "stage": match.stage,
        "group_name": match.group_name,
        "home_score": match.home_score,
        "away_score": match.away_score,
        "status": match.status,
        "venue": match.venue
    }