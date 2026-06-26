"""
Stores the structured fields extracted from a resume's raw text.

One row per Resume (1:1), not per user — since Resume already supports
multiple versions per user, each version gets its own independently
parsed data rather than overwriting a shared record. `skills` is stored
as a comma-joined string rather than a separate join table, matching the
same "simple now, normalize later if needed" tradeoff made for `User.role`.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.database.session import Base


def _generate_uuid() -> str:
    return str(uuid.uuid4())


class ExtractedResumeData(Base):
    __tablename__ = "extracted_resume_data"

    id: Mapped[str] = Column(String, primary_key=True, default=_generate_uuid)
    resume_id: Mapped[str] = Column(
        String, ForeignKey("resumes.id"), nullable=False, unique=True, index=True
    )

    full_name: Mapped[str | None] = Column(String, nullable=True)
    email: Mapped[str | None] = Column(String, nullable=True)
    phone: Mapped[str | None] = Column(String, nullable=True)

    # Comma-joined for simplicity (see module docstring). Always read/written
    # through the skills_list property below, never split/joined manually
    # elsewhere, so the delimiter choice stays in one place.
    skills_csv: Mapped[str] = Column(Text, nullable=False, default="")

    education_raw: Mapped[str | None] = Column(Text, nullable=True)
    experience_raw: Mapped[str | None] = Column(Text, nullable=True)
    projects_raw: Mapped[str | None] = Column(Text, nullable=True)
    certifications_raw: Mapped[str | None] = Column(Text, nullable=True)

    raw_text: Mapped[str] = Column(Text, nullable=False)

    parsed_at: Mapped[datetime] = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    resume = relationship("Resume", backref="extracted_data", uselist=False)

    @property
    def skills_list(self) -> list[str]:
        return [s for s in self.skills_csv.split(",") if s]

    @skills_list.setter
    def skills_list(self, skills: list[str]) -> None:
        self.skills_csv = ",".join(skills)

    # Note: skills_list is a plain Python property, not a mapped column —
    # it can be read/set on an existing instance (resume.skills_list = [...])
    # but it is NOT usable as a constructor kwarg
    # (ExtractedResumeData(skills_list=[...]) raises TypeError) and cannot
    # be used in db.query(...).filter(...) calls. Always construct with
    # skills_csv=",".join(skills) directly, then skills_list is available
    # for convenient reading/writing afterward. See services/parsing_service.py.

    def __repr__(self) -> str:
        return f"<ExtractedResumeData resume_id={self.resume_id} name={self.full_name!r}>"
