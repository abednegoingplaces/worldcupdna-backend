from fastapi import APIRouter
import httpx

router = APIRouter(
    prefix="/api/v1/players",
    tags=["players"]
)

@router.get("/photo/{player_name}")
async def get_player_photo(player_name: str):
    """
    Fetches the player's photo from Wikipedia REST API.
    """
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{player_name}"
    headers = {"User-Agent": "WorldCupDNA/1.0"}
    
    async with httpx.AsyncClient(headers=headers) as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                if "thumbnail" in data and "source" in data["thumbnail"]:
                    return {"photo": data["thumbnail"]["source"]}
        except Exception:
            pass
            
    return {"photo": None}
