"""
Orchestrates resume parsing: raw text extraction -> rule-based field
extraction -> persisted ExtractedResumeData row.

Kept as its own service (not folded into resume_service.py) because
parsing is conceptually a separate step that can fail independently of
upload/storage succeeding — a resume can be uploaded and stored even if
parsing later fails or needs to be re-run.
"""

from sqlalchemy.orm import Session

from app.ai_engine.rule_based_extractor import extract_all_fields
from app.ai_engine.text_extraction import extract_text
from app.models.extracted_resume_data import ExtractedResumeData
from app.models.resume import Resume


def parse_resume(db: Session, resume: Resume, file_bytes: bytes) -> ExtractedResumeData:
    """
    Runs extraction on a resume's file bytes and persists the result.
    If this resume was already parsed before (re-parse case — e.g. the
    extraction logic improved and someone wants fresh results), the
    existing row is updated in place rather than creating a duplicate,
    since resume_id is unique on this table.
    """
    raw_text = extract_text(file_bytes, resume.file_extension)
    fields = extract_all_fields(raw_text)

    existing = (
        db.query(ExtractedResumeData)
        .filter(ExtractedResumeData.resume_id == resume.id)
        .first()
    )

    if existing is not None:
        existing.full_name = fields["full_name"]
        existing.email = fields["email"]
        existing.phone = fields["phone"]
        existing.skills_list = fields["skills"]
        existing.education_raw = fields["education_raw"]
        existing.experience_raw = fields["experience_raw"]
        existing.projects_raw = fields["projects_raw"]
        existing.certifications_raw = fields["certifications_raw"]
        existing.raw_text = raw_text
        db.commit()
        db.refresh(existing)
        return existing

    extracted = ExtractedResumeData(
        resume_id=resume.id,
        full_name=fields["full_name"],
        email=fields["email"],
        phone=fields["phone"],
        skills_csv=",".join(fields["skills"]),
        education_raw=fields["education_raw"],
        experience_raw=fields["experience_raw"],
        projects_raw=fields["projects_raw"],
        certifications_raw=fields["certifications_raw"],
        raw_text=raw_text,
    )
    db.add(extracted)
    db.commit()
    db.refresh(extracted)
    return extracted


def get_extracted_data_for_resume(db: Session, resume_id: str) -> ExtractedResumeData | None:
    return (
        db.query(ExtractedResumeData)
        .filter(ExtractedResumeData.resume_id == resume_id)
        .first()
    )
