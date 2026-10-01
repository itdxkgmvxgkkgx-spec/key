import os
from pydantic_settings import BaseSettings

os.makedirs("data", exist_ok=True)


class Settings(BaseSettings):
    """NovaSeek runtime configuration. All values can be overridden with env vars."""

    APP_NAME: str = "NovaSeek"
    # JWT signing key — set APP_SECRET_KEY in secrets for production
    SECRET_KEY: str = "novaseek-dev-secret-change-me"
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/db.sqlite3"

    # Local SearXNG instance (unlimited, self-hosted metasearch engine)
    SEARXNG_URL: str = "http://localhost:8888"
    SEARCH_TIMEOUT: float = 15.0
    SCRAPE_TIMEOUT: float = 25.0

    # Owner account — credentials come from GitHub Secrets, never hardcoded
    OWNER_USERNAME: str = "owner"
    OWNER_PASSWORD: str = "owner123"

    # Quotas & limits
    DEFAULT_DAILY_QUOTA: int = 1000
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    CACHE_TTL_SECONDS: int = 300
    REGISTRATION_OPEN: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
