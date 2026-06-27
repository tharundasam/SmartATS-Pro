"""
Aggregates every v1 route module under a single router, mounted at
settings.API_V1_PREFIX (default "/api/v1") in app/main.py.

As each module is built, its router is imported and included here:
    from app.api.v1 import auth, resumes, ats, job_match, ...
    api_router.include_router(auth.router, prefix="/auth")
    api_router.include_router(resumes.router, prefix="/resumes")
    api_router.include_router(ats.router, prefix="/ats")
    ...

This keeps main.py stable — it only ever imports `api_router` once,
regardless of how many modules get added underneath it.
"""

from fastapi import APIRouter

from app.api.v1 import ats, auth, health, resumes

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(resumes.router, prefix="/resumes")
api_router.include_router(ats.router, prefix="/ats")
