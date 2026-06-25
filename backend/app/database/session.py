"""
SQLAlchemy engine/session setup.

DATABASE_URL controls the backend entirely:
  - Local dev (default):  sqlite:///./smartats.db
  - Production:            postgresql+psycopg2://user:pass@host:5432/dbname

`connect_args={"check_same_thread": False}` is SQLite-specific (needed
because SQLite by default only allows the thread that created a
connection to use it, which conflicts with FastAPI's threaded request
handling). It's a no-op / not applied for other database backends.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import get_settings

settings = get_settings()

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a DB session and guarantees it's
    closed after the request, even if an exception is raised.

    Usage in a route:
        def my_route(db: Session = Depends(get_db)): ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
