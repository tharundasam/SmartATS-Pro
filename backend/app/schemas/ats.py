from datetime import datetime

from pydantic import BaseModel, Field


class ATSScoreRequest(BaseModel):
    """
    Request body for POST /ats/score/{resume_id}. `job_description` is
    optional — when omitted (or blank), only generic ATS checks run
    (matching the standalone "ATS Score Breakdown" mockup screen);
    when provided, skills/keywords scoring is matched against it
    instead (matching the "Job Match Engine" mockup screen). See
    app/ai_engine/rule_based_scorer.py's module docstring.
    """

    job_description: str | None = Field(
        default=None,
        description=(
            "Optional job description text to match the resume against. "
            "If omitted, only generic ATS checks are run."
        ),
    )


class ATSReportOut(BaseModel):
    """
    Note on `missing_keywords` / `ai_suggestions`: same pattern as
    ExtractedResumeDataOut.skills (see app/schemas/parsing.py docstring)
    — the ORM model (ATSReport) stores these as JSON-encoded text
    columns and exposes plain-Python-property accessors, which
    Pydantic's from_attributes mode won't pick up by name. The route
    handler (api/v1/ats.py) builds this schema explicitly.
    """

    id: str
    resume_id: str
    job_description: str | None
    overall_score: float
    skills_score: float
    keywords_score: float
    formatting_score: float
    education_score: float
    projects_score: float
    missing_keywords: list[str]
    ai_suggestions: list[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ATSReportListResponse(BaseModel):
    total: int
    reports: list[ATSReportOut]
