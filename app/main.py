"""WorldCupDNA API — application entrypoint.

A modular monolith: each domain lives under ``app/modules/<domain>`` with its
own models, schemas, service and router. This file wires those routers together
behind a single FastAPI app and the ``/api/v1`` prefix.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app import models_registry  # noqa: F401  (registers all tables on Base)

# Module routers
from app.modules.admin.router import router as admin_router
from app.modules.auth.router import router as auth_router
from app.modules.leaderboard.router import router as leaderboard_router
from app.modules.matches.router import router as matches_router
from app.modules.notifications.router import router as notifications_router
from app.modules.payments.router import router as payments_router
from app.modules.players.router import router as players_router
from app.modules.predictions.router import router as predictions_router
from app.modules.stats.router import router as stats_router
from app.modules.users.router import router as users_router
from app.modules.venues.router import router as venues_router

# Create tables (idempotent). For schema changes on an existing DB use the
# migration scripts in ``scripts/``.
Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description="FIFA World Cup 2026 fan identity & prediction platform",
        version=settings.APP_VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    routers = [
        auth_router,
        users_router,
        matches_router,
        predictions_router,
        leaderboard_router,
        venues_router,
        notifications_router,
        players_router,
        stats_router,
        payments_router,
        admin_router,
    ]
    for router in routers:
        app.include_router(router, prefix=settings.API_PREFIX)

    @app.get("/", tags=["meta"])
    def root():
        return {
            "message": "WorldCupDNA API is live 🏆",
            "version": settings.APP_VERSION,
            "docs": "/docs",
            "api": settings.API_PREFIX,
        }

    @app.get("/health", tags=["meta"])
    def health():
        return {"status": "healthy", "environment": settings.ENVIRONMENT}

    return app


app = create_app()
