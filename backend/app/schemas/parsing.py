from datetime import datetime

from pydantic import BaseModel


class ExtractedResumeDataOut(BaseModel):
    """
    Note on `skills`: the ORM model (ExtractedResumeData) stores skills as
    a comma-joined string column (`skills_csv`) and exposes a `skills_list`
    Python property for convenience — but Pydantic's `from_attributes`
    mode matches by field name, so it would look for `.skills` on the ORM
    object and fail to find it. Rather than fight that mismatch with a
    validator, the route handler (api/v1/resumes.py) builds this schema
    explicitly with `model_validate(extracted, ...)` overridden via a
    plain dict, passing `skills=extracted.skills_list` directly.
    """

    id: str
    resume_id: str
    full_name: str | None
    email: str | None
    phone: str | None
    skills: list[str]
    education_raw: str | None
    experience_raw: str | None
    projects_raw: str | None
    certifications_raw: str | None
    parsed_at: datetime

    class Config:
        from_attributes = True
