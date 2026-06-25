"""
SmartATS Pro API — application entry point.

Run locally with:
    uvicorn app.main:app --reload

Swagger UI:  http://localhost:8000/docs
ReDoc:       http://localhost:8000/redoc
OpenAPI:     http://localhost:8000/openapi.json
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import get_settings
from app.database.session import Base, engine
from app.schemas.health import RootResponse

# Importing app.models registers every ORM model's table on Base.metadata.
# Without this import, Base.metadata.create_all() below would create zero
# tables — SQLAlchemy only knows about classes that have actually been
# imported somewhere in the process. Every future model module must be
# re-exported from app/models/__init__.py to stay covered by this single
# import.
from app import models  # noqa: F401

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI-Powered Resume Intelligence Platform — backend API. "
        "Final Year Project: SmartATS Pro."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# --- CORS ---
# Allows the React dev server (Vite, default port 5173) to call this API
# directly during local development. In production, CORS_ORIGINS should
# be set to the deployed frontend's exact origin (e.g. Vercel URL).
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
def on_startup() -> None:
    """
    Creates any tables defined on Base.metadata that don't exist yet.
    Safe to call repeatedly — it's a no-op for tables that already exist.

    This is fine for local SQLite development. Once real models exist
    and the project moves to PostgreSQL, this will be replaced by Alembic
    migrations (tracked, reversible schema changes) instead of relying on
    create_all at startup.
    """
    Base.metadata.create_all(bind=engine)


@app.get("/", response_model=RootResponse, tags=["Root"])
def root() -> RootResponse:
    return RootResponse(
        message=f"{settings.APP_NAME} is running.",
        docs_url="/docs",
        api_version=settings.API_V1_PREFIX,
    )
