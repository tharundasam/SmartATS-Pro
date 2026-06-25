"""
Resume upload/storage business logic.

Stored filenames on disk are randomized UUIDs (not the user's original
filename) for two reasons: avoids filesystem collisions when two users
upload a file with the same name, and avoids path-traversal or
special-character issues from untrusted filenames ending up in a path.
The user's original filename is preserved separately in the DB
(`original_filename`) purely for display.
"""

import uuid
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.resume import Resume

settings = get_settings()


def _ensure_upload_dir() -> Path:
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def save_resume_upload(
    db: Session,
    user_id: str,
    original_filename: str,
    extension: str,
    file_bytes: bytes,
) -> Resume:
    upload_dir = _ensure_upload_dir()

    stored_filename = f"{uuid.uuid4()}.{extension}"
    file_path = upload_dir / stored_filename
    file_path.write_bytes(file_bytes)

    # Determine the next version number for this user, and demote any
    # existing "current" resume — exactly one row per user should have
    # is_current=True at a time.
    previous_versions = db.query(Resume).filter(Resume.user_id == user_id)
    latest_version = previous_versions.order_by(Resume.version.desc()).first()
    next_version = (latest_version.version + 1) if latest_version else 1

    previous_versions.filter(Resume.is_current.is_(True)).update({"is_current": False})

    resume = Resume(
        user_id=user_id,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_extension=extension,
        file_size_bytes=len(file_bytes),
        version=next_version,
        is_current=True,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume


def list_resumes_for_user(db: Session, user_id: str) -> list[Resume]:
    return (
        db.query(Resume)
        .filter(Resume.user_id == user_id)
        .order_by(Resume.version.desc())
        .all()
    )


def get_resume_for_user(db: Session, user_id: str, resume_id: str) -> Resume:
    resume = (
        db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == user_id).first()
    )
    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found."
        )
    return resume


def get_resume_file_path(resume: Resume) -> Path:
    return Path(settings.UPLOAD_DIR) / resume.stored_filename


def delete_resume_for_user(db: Session, user_id: str, resume_id: str) -> None:
    resume = get_resume_for_user(db, user_id, resume_id)
    was_current = resume.is_current

    file_path = get_resume_file_path(resume)
    file_path.unlink(missing_ok=True)

    db.delete(resume)
    db.commit()

    # If the deleted resume was the user's current one, promote the
    # next-most-recent remaining version (if any) to current, so the
    # user always has an active resume as long as they have at least one.
    if was_current:
        next_latest = (
            db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.version.desc())
            .first()
        )
        if next_latest is not None:
            next_latest.is_current = True
            db.commit()
