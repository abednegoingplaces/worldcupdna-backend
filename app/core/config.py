"""Centralised application configuration.

All settings are read from environment variables (loaded from a local ``.env``
file in development). Never hard-code secrets — see ``.env.example`` for the
full list of variables the app understands.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- Core ---
    APP_NAME: str = "WorldCupDNA API"
    APP_VERSION: str = "2.0.0"
    ENVIRONMENT: str = "development"
    API_PREFIX: str = "/api/v1"

    # --- Database ---
    DATABASE_URL: str

    # --- Security / JWT ---
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- CORS (comma-separated origins, or "*") ---
    CORS_ORIGINS: str = "*"

    # --- football-data.org ---
    FOOTBALL_API_KEY: str = ""
    FOOTBALL_API_BASE: str = "https://api.football-data.org/v4"
    WORLD_CUP_COMPETITION_ID: int = 2000  # FIFA World Cup (free tier)
    FOOTBALL_CACHE_TTL: int = 60  # seconds — protects the 10 req/min free limit

    # --- StatsBomb (open data is free; paid API needs credentials) ---
    STATSBOMB_USERNAME: str = ""
    STATSBOMB_PASSWORD: str = ""
    STATSBOMB_OPEN_DATA_BASE: str = (
        "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
    )

    # --- Third-party stubs ---
    SENDGRID_API_KEY: str = ""
    STRIPE_SECRET_KEY: str = ""
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        if self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
