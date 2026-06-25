"""
Centralized application settings, loaded from environment variables (.env).

Per project decision: SQLite for local development, PostgreSQL for
production deployment. DATABASE_URL controls which is used — swapping
environments requires no code changes, only a different .env value.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # --- App ---
    APP_NAME: str = "SmartATS Pro API"
    APP_ENV: str = "development"  # development | staging | production
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # --- Database ---
    # SQLite for local dev (default). For production, set e.g.:
    #   postgresql+psycopg2://user:password@host:5432/smartats
    DATABASE_URL: str = "sqlite:///./smartats.db"

    # --- Auth (wired in Phase B Step 2 — present now so .env is stable) ---
    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # --- CORS ---
    # Comma-separated list of allowed origins. The Vite dev server runs on
    # 5173 by default (see frontend/vite.config.ts).
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    # --- File storage (wired in Phase B Step 3) ---
    UPLOAD_DIR: str = "./storage/resumes"
    MAX_UPLOAD_SIZE_MB: int = 10

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — .env is read once per process."""
    return Settings()
