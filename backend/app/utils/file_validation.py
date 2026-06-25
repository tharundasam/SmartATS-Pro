"""
Validation for uploaded resume files.

Three layers of checking, deliberately:
  1. Extension — cheap, first-pass rejection of obviously wrong files.
  2. Size — enforced from settings.MAX_UPLOAD_SIZE_MB.
  3. Magic bytes — the file's actual binary signature, checked against
     what the extension claims. This exists because relying on the
     extension alone means a file named "resume.pdf" that's actually a
     renamed executable would sail through. It's a basic check, not a
     full antivirus scan — flagged here so that distinction is explicit.
"""

from fastapi import HTTPException, UploadFile, status

from app.core.config import get_settings

settings = get_settings()

ALLOWED_EXTENSIONS = {"pdf", "docx"}

# First bytes of a real PDF file are always exactly this.
_PDF_MAGIC = b"%PDF-"
# DOCX is a zip archive; zip files always start with this signature.
_ZIP_MAGIC = b"PK\x03\x04"


def get_extension(filename: str) -> str:
    if "." not in filename:
        return ""
    return filename.rsplit(".", 1)[-1].lower()


def validate_extension(filename: str) -> str:
    extension = get_extension(filename)
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '.{extension}'. Only PDF and DOCX are allowed.",
        )
    return extension


def validate_size(file_size_bytes: int) -> None:
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_size_bytes > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds the {settings.MAX_UPLOAD_SIZE_MB}MB limit.",
        )
    if file_size_bytes == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )


def validate_content_matches_extension(file_bytes: bytes, extension: str) -> None:
    """Sniffs the first few bytes to confirm the file's actual content
    matches what its extension claims, rather than trusting the
    extension/filename alone."""
    if extension == "pdf" and not file_bytes.startswith(_PDF_MAGIC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content does not match a valid PDF.",
        )
    if extension == "docx" and not file_bytes.startswith(_ZIP_MAGIC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File content does not match a valid DOCX.",
        )


async def validate_upload(file: UploadFile) -> tuple[bytes, str]:
    """
    Runs all three checks and returns (file_bytes, extension) on success,
    or raises HTTPException on the first failure.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No filename provided."
        )

    extension = validate_extension(file.filename)

    file_bytes = await file.read()
    validate_size(len(file_bytes))
    validate_content_matches_extension(file_bytes, extension)

    return file_bytes, extension
