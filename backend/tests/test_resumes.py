import io
import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Minimal byte sequences matching the magic-byte checks in
# app/utils/file_validation.py — not fully parseable documents, just
# enough to pass the signature sniff this project performs.
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


def test_upload_pdf_succeeds():
    token = _register_and_get_token()
    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.pdf", io.BytesIO(FAKE_PDF_BYTES), "application/pdf")},
        headers=_auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["original_filename"] == "resume.pdf"
    assert body["file_extension"] == "pdf"
    assert body["version"] == 1
    assert body["is_current"] is True


def test_upload_docx_succeeds():
    token = _register_and_get_token()
    response = client.post(
        "/api/v1/resumes/upload",
        files={
            "file": (
                "resume.docx",
                io.BytesIO(FAKE_DOCX_BYTES),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
        headers=_auth_headers(token),
    )
    assert response.status_code == 201
    assert response.json()["file_extension"] == "docx"


def test_upload_without_auth_returns_401():
    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.pdf", io.BytesIO(FAKE_PDF_BYTES), "application/pdf")},
    )
    assert response.status_code == 401


def test_upload_rejects_disallowed_extension():
    token = _register_and_get_token()
    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.exe", io.BytesIO(FAKE_TXT_BYTES), "application/octet-stream")},
        headers=_auth_headers(token),
    )
    assert response.status_code == 400


def test_upload_rejects_content_mismatched_with_extension():
    """A .pdf filename whose bytes don't actually start with the PDF
    signature should be rejected — this is the renamed-file attack case."""
    token = _register_and_get_token()
    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.pdf", io.BytesIO(FAKE_TXT_BYTES), "application/pdf")},
        headers=_auth_headers(token),
    )
    assert response.status_code == 400


def test_upload_rejects_empty_file():
    token = _register_and_get_token()
    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.pdf", io.BytesIO(b""), "application/pdf")},
        headers=_auth_headers(token),
    )
    assert response.status_code == 400


def test_second_upload_becomes_current_and_increments_version():
    token = _register_and_get_token()
    headers = _auth_headers(token)

    first = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("v1.pdf", io.BytesIO(FAKE_PDF_BYTES), "application/pdf")},
        headers=headers,
    ).json()
    second = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("v2.pdf", io.BytesIO(FAKE_PDF_BYTES), "application/pdf")},
        headers=headers,
    ).json()

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
        client.post(
            "/api/v1/resumes/upload",
            files={"file": (name, io.BytesIO(FAKE_PDF_BYTES), "application/pdf")},
            headers=headers,
        )

    response = client.get("/api/v1/resumes", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 3
    versions = [r["version"] for r in body["resumes"]]
    assert versions == [3, 2, 1]


def test_download_returns_file_content():
    token = _register_and_get_token()
    headers = _auth_headers(token)

    uploaded = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("download-me.pdf", io.BytesIO(FAKE_PDF_BYTES), "application/pdf")},
        headers=headers,
    ).json()

    response = client.get(f"/api/v1/resumes/{uploaded['id']}/download", headers=headers)
    assert response.status_code == 200
    assert response.content == FAKE_PDF_BYTES


def test_users_cannot_access_each_others_resumes():
    token_a = _register_and_get_token()
    token_b = _register_and_get_token()

    uploaded = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("private.pdf", io.BytesIO(FAKE_PDF_BYTES), "application/pdf")},
        headers=_auth_headers(token_a),
    ).json()

    response = client.get(f"/api/v1/resumes/{uploaded['id']}", headers=_auth_headers(token_b))
    assert response.status_code == 404


def test_delete_resume_removes_it_and_promotes_previous_version():
    token = _register_and_get_token()
    headers = _auth_headers(token)

    first = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("first.pdf", io.BytesIO(FAKE_PDF_BYTES), "application/pdf")},
        headers=headers,
    ).json()
    second = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("second.pdf", io.BytesIO(FAKE_PDF_BYTES), "application/pdf")},
        headers=headers,
    ).json()

    delete_response = client.delete(f"/api/v1/resumes/{second['id']}", headers=headers)
    assert delete_response.status_code == 204

    # The deleted resume is gone...
    get_response = client.get(f"/api/v1/resumes/{second['id']}", headers=headers)
    assert get_response.status_code == 404

    # ...and the previous version is now current.
    first_metadata = client.get(f"/api/v1/resumes/{first['id']}", headers=headers).json()
    assert first_metadata["is_current"] is True
