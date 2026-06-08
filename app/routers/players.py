from fastapi import APIRouter
import httpx

router = APIRouter(
    prefix="/api/v1/players",
    tags=["players"]
)

@router.get("/photo/{player_name}")
async def get_player_photo(player_name: str):
    """
    Fetches the player's photo from TheSportsDB API.
    """
    name = player_name.replace("_", " ")
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p={name}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("player") and len(data["player"]) > 0:
                    thumb = data["player"][0].get("strThumb")
                    if thumb:
                        return {"photo": thumb}
        except Exception:
            pass

    return {"photo": None}
