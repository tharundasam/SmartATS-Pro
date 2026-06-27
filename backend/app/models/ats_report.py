"""
ATSReport model — persists the result of one ATS scoring run.

Design choice: one row per scoring *run*, not per resume. A user can
re-score the same resume against different job descriptions, or re-run
a generic (no-JD) check after editing their resume — each call creates
a new row rather than overwriting a previous result. This is what
powers a score-over-time trend (see the dashboard mockup's "ATS
Evolution" chart) and lets a user compare how the same resume version
scored against several different job postings.

Sub-scores and missing keywords are stored as comma-joined / JSON-ish
text columns (TEXT), matching the same "simple now, normalize later if
needed" tradeoff already used for `ExtractedResumeData.skills_csv` and
`User.role`. Missing keywords specifically are stored as JSON text
(via Python's json module) rather than comma-joined, since keyword
phrases themselves can legitimately contain commas/spaces (e.g.
"CI/CD Pipelines") and JSON round-trips that safely without choosing a
delimiter that could collide with real content.
"""

import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.database.session import Base


def _generate_uuid() -> str:
    return str(uuid.uuid4())


class ATSReport(Base):
    __tablename__ = "ats_reports"

    id: Mapped[str] = Column(String, primary_key=True, default=_generate_uuid)
    resume_id: Mapped[str] = Column(
        String, ForeignKey("resumes.id"), nullable=False, index=True
    )
    user_id: Mapped[str] = Column(
        String, ForeignKey("users.id"), nullable=False, index=True
    )

    # Null when this report was a generic (no-JD) check, matching the
    # standalone "ATS Score Breakdown" mockup screen rather than the
    # "Job Match Engine" screen. Stored in full (not just a flag) so a
    # user can revisit exactly what JD a past report was scored against.
    job_description: Mapped[str | None] = Column(Text, nullable=True)

    overall_score: Mapped[float] = Column(Float, nullable=False)
    skills_score: Mapped[float] = Column(Float, nullable=False)
    formatting_score: Mapped[float] = Column(Float, nullable=False)
    keywords_score: Mapped[float] = Column(Float, nullable=False)
    education_score: Mapped[float] = Column(Float, nullable=False)
    projects_score: Mapped[float] = Column(Float, nullable=False)

    # JSON-encoded list[str]. Always read/written through the
    # missing_keywords_list property below — see module docstring.
    missing_keywords_json: Mapped[str] = Column(Text, nullable=False, default="[]")

    # JSON-encoded list[str]. Plain-language, user-facing suggestions —
    # currently produced by a stubbed placeholder (see
    # app/ai_engine/llm_suggestions.py), structured so a real LLM call
    # can be swapped in later without changing this column's shape.
    ai_suggestions_json: Mapped[str] = Column(Text, nullable=False, default="[]")

    created_at: Mapped[datetime] = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    resume = relationship("Resume", backref="ats_reports")
    user = relationship("User", backref="ats_reports")

    @property
    def missing_keywords(self) -> list[str]:
        return json.loads(self.missing_keywords_json)

    @missing_keywords.setter
    def missing_keywords(self, keywords: list[str]) -> None:
        self.missing_keywords_json = json.dumps(keywords)

    @property
    def ai_suggestions(self) -> list[str]:
        return json.loads(self.ai_suggestions_json)

    @ai_suggestions.setter
    def ai_suggestions(self, suggestions: list[str]) -> None:
        self.ai_suggestions_json = json.dumps(suggestions)

    # Note: missing_keywords / ai_suggestions are plain Python properties,
    # not mapped columns — same caveat as ExtractedResumeData.skills_list
    # (see that model's docstring). Construct with
    # missing_keywords_json=json.dumps([...]) directly; the properties are
    # for convenient reading/writing afterward. See services/ats_service.py.

    def __repr__(self) -> str:
        return (
            f"<ATSReport id={self.id} resume_id={self.resume_id} "
            f"overall={self.overall_score}>"
        )
