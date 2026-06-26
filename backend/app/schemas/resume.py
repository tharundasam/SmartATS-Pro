from datetime import datetime

from pydantic import BaseModel

from app.schemas.parsing import ExtractedResumeDataOut


class ResumeOut(BaseModel):
    id: str
    original_filename: str
    file_extension: str
    file_size_bytes: int
    version: int
    is_current: bool
    uploaded_at: datetime

    class Config:
        from_attributes = True


class ResumeListResponse(BaseModel):
    total: int
    resumes: list[ResumeOut]


class ResumeUploadResponse(BaseModel):
    """
    Response shape for POST /resumes/upload as of Phase B Step 4.

    Note: this changes the upload endpoint's response shape from Step 3,
    which returned a bare ResumeOut. The resume's own fields are now
    nested under `resume` instead of being top-level. If your frontend
    already has code reading the upload response directly as a flat
    object (e.g. `response.data.version`), it needs to change to
    `response.data.resume.version`. See the backend README's Step 4
    section for the exact before/after shape.
    """

    resume: ResumeOut
    extracted_data: ExtractedResumeDataOut | None
    parsing_error: str | None = None
