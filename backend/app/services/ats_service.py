"""
Orchestrates ATS scoring: load a resume's extracted data -> run the
rule-based scorer -> run (currently stubbed) AI suggestions -> persist
an ATSReport row.

Kept as its own service (not folded into parsing_service.py or
resume_service.py) for the same reason parsing is split out from
upload — scoring is a distinct step that depends on parsing having
already succeeded, and can be re-run independently (e.g. against a
new job description) without re-uploading or re-parsing anything.
"""

import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.ai_engine.llm_suggestions import generate_ai_suggestions
from app.ai_engine.rule_based_scorer import run_rule_based_scoring
from app.models.ats_report import ATSReport
from app.models.extracted_resume_data import ExtractedResumeData
from app.models.resume import Resume


def score_resume(
    db: Session,
    resume: Resume,
    job_description: str | None,
) -> ATSReport:
    """
    Scores a resume (optionally against a job description) and
    persists the result as a new ATSReport row. Raises 404 if the
    resume hasn't been successfully parsed yet — scoring depends on
    ExtractedResumeData existing, same dependency parsing has on the
    resume file itself existing.
    """
    extracted = (
        db.query(ExtractedResumeData)
        .filter(ExtractedResumeData.resume_id == resume.id)
        .first()
    )
    if extracted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "This resume has not been successfully parsed yet, so it "
                "can't be scored. Try POST /resumes/{resume_id}/reparse "
                "first, or check the original upload's parsing_error."
            ),
        )

    normalized_jd = job_description.strip() if job_description and job_description.strip() else None

    scoring_result = run_rule_based_scoring(
        raw_text=extracted.raw_text,
        skills=extracted.skills_list,
        education_raw=extracted.education_raw,
        experience_raw=extracted.experience_raw,
        projects_raw=extracted.projects_raw,
        certifications_raw=extracted.certifications_raw,
        job_description=normalized_jd,
    )

    sub_scores = {
        "skills_score": scoring_result["skills_score"],
        "keywords_score": scoring_result["keywords_score"],
        "formatting_score": scoring_result["formatting_score"],
        "education_score": scoring_result["education_score"],
        "projects_score": scoring_result["projects_score"],
    }
    ai_suggestions = generate_ai_suggestions(
        raw_text=extracted.raw_text,
        job_description=normalized_jd,
        sub_scores=sub_scores,
        missing_keywords=scoring_result["missing_keywords"],
    )

    report = ATSReport(
        resume_id=resume.id,
        user_id=resume.user_id,
        job_description=normalized_jd,
        overall_score=scoring_result["overall_score"],
        skills_score=scoring_result["skills_score"],
        keywords_score=scoring_result["keywords_score"],
        formatting_score=scoring_result["formatting_score"],
        education_score=scoring_result["education_score"],
        projects_score=scoring_result["projects_score"],
        missing_keywords_json=json.dumps(scoring_result["missing_keywords"]),
        ai_suggestions_json=json.dumps(ai_suggestions),
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def list_reports_for_resume(db: Session, user_id: str, resume_id: str) -> list[ATSReport]:
    """Most recent first — matches list_resumes_for_user's ordering
    convention in resume_service.py, and is what a trend chart would
    want to render in reverse (or the caller can .reverse() as needed)."""
    return (
        db.query(ATSReport)
        .filter(ATSReport.resume_id == resume_id, ATSReport.user_id == user_id)
        .order_by(ATSReport.created_at.desc())
        .all()
    )


def get_report_for_user(db: Session, user_id: str, report_id: str) -> ATSReport:
    report = (
        db.query(ATSReport)
        .filter(ATSReport.id == report_id, ATSReport.user_id == user_id)
        .first()
    )
    if report is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ATS report not found."
        )
    return report
