from datetime import datetime

from pydantic import BaseModel


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
