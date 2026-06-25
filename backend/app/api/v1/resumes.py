from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.resume import ResumeListResponse, ResumeOut
from app.services.resume_service import (
    delete_resume_for_user,
    get_resume_file_path,
    get_resume_for_user,
    list_resumes_for_user,
    save_resume_upload,
)
from app.utils.file_validation import validate_upload

router = APIRouter(tags=["Resumes"])


@router.post("/upload", response_model=ResumeOut, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ResumeOut:
    """
    Uploads a new resume (PDF or DOCX, max size from settings). Becomes
    the user's new "current" version automatically — previous uploads are
    kept (not deleted) for version history.
    """
    file_bytes, extension = await validate_upload(file)
    # validate_upload already raised if file.filename was empty/None, so
    # this assertion is purely to satisfy static type checkers — it's a
    # no-op at runtime.
    assert file.filename is not None
    resume = save_resume_upload(
        db=db,
        user_id=current_user.id,
        original_filename=file.filename,
        extension=extension,
        file_bytes=file_bytes,
    )
    return ResumeOut.model_validate(resume)


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
