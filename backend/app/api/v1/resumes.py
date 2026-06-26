from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.parsing import ExtractedResumeDataOut
from app.schemas.resume import ResumeListResponse, ResumeOut, ResumeUploadResponse
from app.services.parsing_service import get_extracted_data_for_resume, parse_resume
from app.services.resume_service import (
    delete_resume_for_user,
    get_resume_file_path,
    get_resume_for_user,
    list_resumes_for_user,
    save_resume_upload,
)
from app.utils.file_validation import validate_upload

router = APIRouter(tags=["Resumes"])


def _to_extracted_out(extracted) -> ExtractedResumeDataOut:
    """
    Builds the response schema explicitly rather than via
    model_validate(extracted) directly, because the ORM model exposes
    skills through a `skills_list` property while the schema field is
    named `skills` — from_attributes matching is by name, so it
    wouldn't find it automatically. See schemas/parsing.py docstring.
    """
    return ExtractedResumeDataOut(
        id=extracted.id,
        resume_id=extracted.resume_id,
        full_name=extracted.full_name,
        email=extracted.email,
        phone=extracted.phone,
        skills=extracted.skills_list,
        education_raw=extracted.education_raw,
        experience_raw=extracted.experience_raw,
        projects_raw=extracted.projects_raw,
        certifications_raw=extracted.certifications_raw,
        parsed_at=extracted.parsed_at,
    )


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ResumeUploadResponse:
    """
    Uploads a new resume (PDF or DOCX, max size from settings). Becomes
    the user's new "current" version automatically — previous uploads are
    kept (not deleted) for version history.

    Parsing runs automatically right after a successful upload, using the
    same file bytes already in memory (no second disk read). If parsing
    fails — e.g. a scanned PDF with no selectable text — the upload still
    succeeds; `parsing_error` is set and `extracted_data` is null instead
    of the whole request failing, since a parsing limitation shouldn't
    block the user from having their file stored.
    """
    file_bytes, extension = await validate_upload(file)
    assert file.filename is not None
    resume = save_resume_upload(
        db=db,
        user_id=current_user.id,
        original_filename=file.filename,
        extension=extension,
        file_bytes=file_bytes,
    )

    extracted_out: ExtractedResumeDataOut | None = None
    parsing_error: str | None = None
    try:
        extracted = parse_resume(db, resume, file_bytes)
        extracted_out = _to_extracted_out(extracted)
    except HTTPException as exc:
        # extract_text raises HTTPException(422) for unreadable content
        # (scanned/password-protected/corrupted). Caught here rather than
        # letting it propagate, since the resume itself was saved fine —
        # only parsing failed.
        parsing_error = exc.detail

    return ResumeUploadResponse(
        resume=ResumeOut.model_validate(resume),
        extracted_data=extracted_out,
        parsing_error=parsing_error,
    )


@router.get("", response_model=ResumeListResponse)
def list_my_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ResumeListResponse:
    """Lists every version of the current user's resume, most recent first."""
    resumes = list_resumes_for_user(db, current_user.id)
    return ResumeListResponse(
        total=len(resumes), resumes=[ResumeOut.model_validate(r) for r in resumes]
    )


@router.get("/{resume_id}", response_model=ResumeOut)
def get_resume_metadata(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ResumeOut:
    """Returns metadata for one resume. Users can only access their own resumes —
    a mismatched user_id/resume_id pair returns 404, not 403, so as to not
    confirm whether a given resume_id exists at all to someone who doesn't own it."""
    resume = get_resume_for_user(db, current_user.id, resume_id)
    return ResumeOut.model_validate(resume)


@router.get("/{resume_id}/parsed-data", response_model=ExtractedResumeDataOut)
def get_parsed_data(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExtractedResumeDataOut:
    """
    Returns the structured fields extracted from this resume. 404 if the
    resume itself doesn't exist (or isn't this user's), and a distinct
    404 if the resume exists but was never successfully parsed (e.g. the
    original upload's parsing failed — see `parsing_error` on the upload
    response, or call POST /{resume_id}/reparse to try again).
    """
    get_resume_for_user(db, current_user.id, resume_id)  # ownership/existence check
    extracted = get_extracted_data_for_resume(db, resume_id)
    if extracted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This resume has not been successfully parsed yet.",
        )
    return _to_extracted_out(extracted)


@router.post("/{resume_id}/reparse", response_model=ExtractedResumeDataOut)
def reparse_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ExtractedResumeDataOut:
    """
    Re-runs extraction on an already-uploaded resume, reading the stored
    file from disk rather than requiring a re-upload. Useful both for
    retrying a resume whose initial parse failed, and for re-extracting
    after the extraction logic itself improves.
    """
    resume = get_resume_for_user(db, current_user.id, resume_id)
    file_path = get_resume_file_path(resume)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The stored file for this resume could not be found on disk.",
        )
    file_bytes = file_path.read_bytes()
    extracted = parse_resume(db, resume, file_bytes)
    return _to_extracted_out(extracted)


@router.get("/{resume_id}/download")
def download_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FileResponse:
    """Streams the original file back, with its original filename and correct
    content-type, so downloading it from the frontend round-trips correctly."""
    resume = get_resume_for_user(db, current_user.id, resume_id)
    file_path = get_resume_file_path(resume)

    media_type = "application/pdf" if resume.file_extension == "pdf" else (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    return FileResponse(
        path=file_path,
        filename=resume.original_filename,
        media_type=media_type,
    )


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Deletes a resume version. If it was the user's current resume, the
    next-most-recent remaining version is automatically promoted to current."""
    delete_resume_for_user(db, current_user.id, resume_id)
