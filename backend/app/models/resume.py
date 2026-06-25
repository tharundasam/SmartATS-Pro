"""
Resume model.

Versioning design: every upload creates a *new* row rather than
overwriting an old one. `version` is a per-user incrementing counter
(1, 2, 3, ... for that specific user, not global), and `is_current`
marks which version is the user's active/default resume. This means:
  - Old versions are never deleted automatically — full history is kept,
    matching the spec's "Resume Versioning" requirement.
  - Exactly one row per user has is_current=True at any time (enforced
    in the service layer, not a DB constraint, since SQLite's partial
    unique indexes are awkward to manage via SQLAlchemy across both
    SQLite and Postgres).
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.database.session import Base


def _generate_uuid() -> str:
    return str(uuid.uuid4())


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[str] = Column(String, primary_key=True, default=_generate_uuid)
    user_id: Mapped[str] = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    original_filename: Mapped[str] = Column(String, nullable=False)
    stored_filename: Mapped[str] = Column(String, nullable=False, unique=True)
    file_extension: Mapped[str] = Column(String, nullable=False)  # "pdf" | "docx"
    file_size_bytes: Mapped[int] = Column(Integer, nullable=False)

    version: Mapped[int] = Column(Integer, nullable=False, default=1)
    is_current: Mapped[bool] = Column(Boolean, nullable=False, default=True)

    uploaded_at: Mapped[datetime] = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    owner = relationship("User", backref="resumes")

    def __repr__(self) -> str:
        return f"<Resume id={self.id} user_id={self.user_id} v{self.version} current={self.is_current}>"
