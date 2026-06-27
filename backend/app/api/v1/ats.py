from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.ats_report import ATSReport
from app.models.user import User
from app.schemas.ats import ATSReportListResponse, ATSReportOut, ATSScoreRequest
from app.services.ats_service import (
    get_report_for_user,
    list_reports_for_resume,
    score_resume,
)
from app.services.resume_service import get_resume_for_user

router = APIRouter(tags=["ATS Scoring"])


def _to_report_out(report: ATSReport) -> ATSReportOut:
    """
    Builds the response schema explicitly rather than via
    model_validate(report) directly, since missing_keywords/
    ai_suggestions are plain Python properties on the ORM model, not
    mapped columns — see schemas/ats.py docstring.
    """
    return ATSReportOut(
        id=report.id,
        resume_id=report.resume_id,
        job_description=report.job_description,
        overall_score=report.overall_score,
        skills_score=report.skills_score,
        keywords_score=report.keywords_score,
        formatting_score=report.formatting_score,
        education_score=report.education_score,
        projects_score=report.projects_score,
        missing_keywords=report.missing_keywords,
        ai_suggestions=report.ai_suggestions,
        created_at=report.created_at,
    )


@router.post("/score/{resume_id}", response_model=ATSReportOut, status_code=201)
def score_resume_endpoint(
    resume_id: str,
    payload: ATSScoreRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ATSReportOut:
    """
    Scores a resume and persists the result as a new report.

    `job_description` in the request body is optional:
      - Omitted/blank: runs generic ATS checks only (formatting,
        education, projects, overall skill breadth) — matches the
        standalone "ATS Score Breakdown" screen.
      - Provided: skills/keyword sub-scores are matched against the
        JD's content instead, and `missing_keywords` is populated with
        terms from the JD not found in the resume — matches the
        "Job Match Engine" screen.

    Each call creates a new report rather than overwriting a previous
    one, so a resume's score history (e.g. across edits, or against
    different job postings) is preserved — see GET /ats/reports/{resume_id}.

    404 if this resume hasn't been successfully parsed yet (scoring
    depends on extracted data existing — see
    POST /resumes/{resume_id}/reparse).
    """
    resume = get_resume_for_user(db, current_user.id, resume_id)
    report = score_resume(db, resume, payload.job_description)
    return _to_report_out(report)


@router.get("/reports/{resume_id}", response_model=ATSReportListResponse)
def list_reports_for_resume_endpoint(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ATSReportListResponse:
    """
    Lists every past scoring run for this resume, most recent first —
    this is what a score-over-time trend (see the dashboard mockup's
    "ATS Evolution" chart) would be built from.

    404 if the resume itself doesn't exist (or isn't this user's). An
    empty `reports` list (not a 404) is returned if the resume exists
    but has never been scored.
    """
    get_resume_for_user(db, current_user.id, resume_id)  # ownership/existence check
    reports = list_reports_for_resume(db, current_user.id, resume_id)
    return ATSReportListResponse(
        total=len(reports), reports=[_to_report_out(r) for r in reports]
    )


@router.get("/reports/{resume_id}/{report_id}", response_model=ATSReportOut)
def get_single_report_endpoint(
    resume_id: str,
    report_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ATSReportOut:
    """
    Returns one specific past report in full. `resume_id` in the path
    is used only for ownership-scoped routing consistency with the
    other resume-nested endpoints; the report itself is looked up (and
    ownership-checked) by `report_id` and the current user.
    """
    get_resume_for_user(db, current_user.id, resume_id)  # ownership/existence check
    report = get_report_for_user(db, current_user.id, report_id)
    return _to_report_out(report)
