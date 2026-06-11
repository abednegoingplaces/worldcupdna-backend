"""Sync World Cup fixtures & results from football-data.org into the DB.

Run:  python -m scripts.sync_matches

Run this on a schedule (e.g. a cron / Render cron job every few minutes during
the tournament) to keep scores and statuses fresh. The free tier allows 10
requests/minute, and this performs a single competition-wide request.
"""
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app import models_registry  # noqa: F401
from app.modules.matches import service


def main() -> None:
    if not settings.FOOTBALL_API_KEY:
        raise SystemExit("FOOTBALL_API_KEY is not set — cannot sync matches.")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        count = service.sync_world_cup(db)
        print(f"✅ Synced {count} World Cup matches from football-data.org")
    finally:
        db.close()


if __name__ == "__main__":
    main()
