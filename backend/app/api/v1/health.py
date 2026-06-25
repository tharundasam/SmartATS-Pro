from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.schemas.health import HealthCheckResponse

router = APIRouter(tags=["Health"])
settings = get_settings()


@router.get("/health", response_model=HealthCheckResponse)
def health_check(db: Session = Depends(get_db)) -> HealthCheckResponse:
    """
    Liveness/readiness check. Runs a trivial query against the real
    database connection (not a hardcoded "ok") so this endpoint actually
    catches a broken DATABASE_URL or an unreachable Postgres instance
    once deployed.
    """
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "unreachable"

    return HealthCheckResponse(
        status="ok" if db_status == "connected" else "degraded",
        app_name=settings.APP_NAME,
        environment=settings.APP_ENV,
        database=db_status,
    )
