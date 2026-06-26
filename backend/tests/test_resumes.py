import io
import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Minimal byte sequences matching the magic-byte checks in
# app/utils/file_validation.py — not fully parseable documents, just
# enough to pass the signature sniff this project performs. Since these
# have no real extractable text, every upload using them will succeed
# with parsing_error set and extracted_data null (see test_parsing.py
# for fixtures that DO parse successfully, used to test the Step 4
# extraction pipeline itself).
FAKE_PDF_BYTES = b"%PDF-1.4\n%%EOF"
FAKE_DOCX_BYTES = b"PK\x03\x04" + b"\x00" * 20  # zip signature + padding
FAKE_TXT_BYTES = b"this is not a pdf or docx"


def _register_and_get_token(role: str = "student") -> str:
    email = f"resume-test-{uuid.uuid4().hex[:10]}@example.com"
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Resume Tester", "email": email, "password": "supersecret123", "role": role},
    )
    return response.json()["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _upload(headers: dict[str, str], filename: str, content: bytes, content_type: str) -> dict:
    """
    Uploads a file and returns the `resume` sub-object directly, since
    every test in this file only cares about resume metadata (not
    parsing results — see test_parsing.py for that). This keeps the
    nested-response shape (introduced in Phase B Step 4) from cluttering
    every single test below with `["resume"]`.
    """
    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": (filename, io.BytesIO(content), content_type)},
        headers=headers,
    )
    return response


def test_upload_pdf_succeeds():
    token = _register_and_get_token()
    response = _upload(_auth_headers(token), "resume.pdf", FAKE_PDF_BYTES, "application/pdf")
    assert response.status_code == 201
    body = response.json()
    resume = body["resume"]
    assert resume["original_filename"] == "resume.pdf"
    assert resume["file_extension"] == "pdf"
    assert resume["version"] == 1
    assert resume["is_current"] is True
    # FAKE_PDF_BYTES has no real text content, so parsing is expected to
    # fail gracefully rather than block the upload — see Step 4 design.
    assert body["extracted_data"] is None
    assert body["parsing_error"] is not None


def test_upload_docx_succeeds():
    token = _register_and_get_token()
    response = _upload(
        _auth_headers(token),
        "resume.docx",
        FAKE_DOCX_BYTES,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    assert response.status_code == 201
    assert response.json()["resume"]["file_extension"] == "docx"


def test_upload_without_auth_returns_401():
    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.pdf", io.BytesIO(FAKE_PDF_BYTES), "application/pdf")},
    )
    assert response.status_code == 401


def test_upload_rejects_disallowed_extension():
    token = _register_and_get_token()
    response = _upload(
        _auth_headers(token), "resume.exe", FAKE_TXT_BYTES, "application/octet-stream"
    )
    assert response.status_code == 400


def test_upload_rejects_content_mismatched_with_extension():
    """A .pdf filename whose bytes don't actually start with the PDF
    signature should be rejected — this is the renamed-file attack case."""
    token = _register_and_get_token()
    response = _upload(_auth_headers(token), "resume.pdf", FAKE_TXT_BYTES, "application/pdf")
    assert response.status_code == 400


def test_upload_rejects_empty_file():
    token = _register_and_get_token()
    response = _upload(_auth_headers(token), "resume.pdf", b"", "application/pdf")
    assert response.status_code == 400


def test_second_upload_becomes_current_and_increments_version():
    token = _register_and_get_token()
    headers = _auth_headers(token)

    first = _upload(headers, "v1.pdf", FAKE_PDF_BYTES, "application/pdf").json()["resume"]
    second = _upload(headers, "v2.pdf", FAKE_PDF_BYTES, "application/pdf").json()["resume"]

    assert first["version"] == 1
    assert second["version"] == 2
    assert second["is_current"] is True

    # The first upload should no longer be current after the second lands.
    first_metadata = client.get(f"/api/v1/resumes/{first['id']}", headers=headers).json()
    assert first_metadata["is_current"] is False


def test_list_resumes_returns_all_versions_most_recent_first():
    token = _register_and_get_token()
    headers = _auth_headers(token)

    for name in ["a.pdf", "b.pdf", "c.pdf"]:
        _upload(headers, name, FAKE_PDF_BYTES, "application/pdf")

    response = client.get("/api/v1/resumes", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    versions = [r["version"] for r in body["resumes"]]
    assert versions == [3, 2, 1]


def test_download_returns_file_content():
    token = _register_and_get_token()
    headers = _auth_headers(token)

    uploaded = _upload(headers, "download-me.pdf", FAKE_PDF_BYTES, "application/pdf").json()["resume"]

    response = client.get(f"/api/v1/resumes/{uploaded['id']}/download", headers=headers)
    assert response.status_code == 200
    assert response.content == FAKE_PDF_BYTES


def test_users_cannot_access_each_others_resumes():
    token_a = _register_and_get_token()
    token_b = _register_and_get_token()

    uploaded = _upload(
        _auth_headers(token_a), "private.pdf", FAKE_PDF_BYTES, "application/pdf"
    ).json()["resume"]

    response = client.get(f"/api/v1/resumes/{uploaded['id']}", headers=_auth_headers(token_b))
    assert response.status_code == 404


def test_delete_resume_removes_it_and_promotes_previous_version():
    token = _register_and_get_token()
    headers = _auth_headers(token)

    first = _upload(headers, "first.pdf", FAKE_PDF_BYTES, "application/pdf").json()["resume"]
    second = _upload(headers, "second.pdf", FAKE_PDF_BYTES, "application/pdf").json()["resume"]

    delete_response = client.delete(f"/api/v1/resumes/{second['id']}", headers=headers)
    assert delete_response.status_code == 204

    # The deleted resume is gone...
    get_response = client.get(f"/api/v1/resumes/{second['id']}", headers=headers)
    assert get_response.status_code == 404

    # ...and the previous version is now current.
    first_metadata = client.get(f"/api/v1/resumes/{first['id']}", headers=headers).json()
    assert first_metadata["is_current"] is True
