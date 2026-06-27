import io
import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Real, parseable resume text — reuses the same hand-built minimal PDF
# approach as test_parsing.py, with content tailored to exercise both
# strong skill coverage and a deliberately thin section (no
# certifications), so generic scoring has visible variation to assert on.
_STRONG_RESUME_TEXT = (
    "Jordan Lee\n"
    "jordan.lee@example.com\n"
    "555-123-4567\n\n"
    "Skills\n"
    "Python, React, AWS, Docker, Kubernetes, PostgreSQL, Git, REST API\n\n"
    "Education\n"
    "B.Sc. Computer Science, State University, 2022\n\n"
    "Experience\n"
    "Software Engineer at Acme Corp, 2022-Present\n\n"
    "Projects\n"
    "Built a microservices-based inventory system using Docker and Kubernetes.\n"
)

_SPARSE_RESUME_TEXT = "Jordan Lee\njordan.lee@example.com\n"

_JD_TEXT = (
    "We are looking for a Software Engineer with strong experience in "
    "Python, Kubernetes, and Microservices. Familiarity with Terraform "
    "and CI/CD pipelines is a plus. The ideal candidate has excellent "
    "communication skills and experience with Agile methodologies."
)


def _build_minimal_pdf_bytes(text: str) -> bytes:
    """Identical fixture builder to test_parsing.py — duplicated rather
    than imported, since tests should not depend on each other's
    internals staying stable."""
    lines = text.split("\n")
    content_lines = ["BT", "/F1 12 Tf", "50 750 Td", "14 TL"]
    for line in lines:
        escaped = line.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
        content_lines.append(f"({escaped}) Tj")
        content_lines.append("T*")
    content_lines.append("ET")
    content_stream = "\n".join(content_lines).encode("latin-1")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> "
        b"/MediaBox [0 0 612 792] /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content_stream)).encode() + b" >>\nstream\n"
        + content_stream + b"\nendstream",
    ]

    pdf = io.BytesIO()
    pdf.write(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(pdf.tell())
        pdf.write(f"{i} 0 obj\n".encode())
        pdf.write(obj)
        pdf.write(b"\nendobj\n")

    xref_offset = pdf.tell()
    pdf.write(f"xref\n0 {len(objects) + 1}\n".encode())
    pdf.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.write(f"{offset:010d} 00000 n \n".encode())
    pdf.write(b"trailer\n")
    pdf.write(f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n".encode())
    pdf.write(b"startxref\n")
    pdf.write(f"{xref_offset}\n".encode())
    pdf.write(b"%%EOF")

    return pdf.getvalue()


def _register_and_get_token() -> str:
    email = f"ats-test-{uuid.uuid4().hex[:10]}@example.com"
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "ATS Tester", "email": email, "password": "supersecret123", "role": "student"},
    )
    return response.json()["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _upload_resume(headers: dict[str, str], text: str, filename: str = "resume.pdf") -> str:
    pdf_bytes = _build_minimal_pdf_bytes(text)
    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": (filename, io.BytesIO(pdf_bytes), "application/pdf")},
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()["resume"]["id"]


def test_generic_score_with_no_job_description():
    token = _register_and_get_token()
    headers = _auth_headers(token)
    resume_id = _upload_resume(headers, _STRONG_RESUME_TEXT)

    response = client.post(
        f"/api/v1/ats/score/{resume_id}", json={}, headers=headers
    )
    assert response.status_code == 201
    body = response.json()

    assert body["resume_id"] == resume_id
    assert body["job_description"] is None
    assert 0.0 <= body["overall_score"] <= 100.0
    assert body["missing_keywords"] == []
    assert isinstance(body["ai_suggestions"], list)
    assert len(body["ai_suggestions"]) > 0
    # Strong resume with all sections present should score well on
    # formatting/education/projects.
    assert body["formatting_score"] > 50
    assert body["education_score"] == 100.0
    assert body["projects_score"] == 100.0


def test_sparse_resume_scores_lower_than_strong_resume():
    token = _register_and_get_token()
    headers = _auth_headers(token)

    strong_id = _upload_resume(headers, _STRONG_RESUME_TEXT, "strong.pdf")
    sparse_id = _upload_resume(headers, _SPARSE_RESUME_TEXT, "sparse.pdf")

    strong_response = client.post(f"/api/v1/ats/score/{strong_id}", json={}, headers=headers)
    sparse_response = client.post(f"/api/v1/ats/score/{sparse_id}", json={}, headers=headers)

    assert strong_response.status_code == 201
    assert sparse_response.status_code == 201
    assert strong_response.json()["overall_score"] > sparse_response.json()["overall_score"]
    assert sparse_response.json()["education_score"] == 0.0
    assert sparse_response.json()["projects_score"] == 0.0


def test_score_with_job_description_populates_missing_keywords():
    token = _register_and_get_token()
    headers = _auth_headers(token)
    resume_id = _upload_resume(headers, _STRONG_RESUME_TEXT)

    response = client.post(
        f"/api/v1/ats/score/{resume_id}",
        json={"job_description": _JD_TEXT},
        headers=headers,
    )
    assert response.status_code == 201
    body = response.json()

    assert body["job_description"] == _JD_TEXT
    # "terraform" and "ci/cd" are in the JD's skill vocabulary but not in
    # the resume's skills list -> should surface as missing.
    assert "terraform" in body["missing_keywords"] or "ci/cd" in body["missing_keywords"]
    # "python" and "kubernetes" ARE in the resume -> should not be listed
    # as missing skills.
    assert "python" not in body["missing_keywords"]
    assert "kubernetes" not in body["missing_keywords"]


def test_score_for_unparsed_resume_returns_404():
    """A resume that failed to parse (extracted_data is null) has
    nothing for the scorer to read, so scoring it should 404 rather
    than crash or silently score empty data."""
    token = _register_and_get_token()
    headers = _auth_headers(token)
    minimal_invalid_pdf = b"%PDF-1.4\n%%EOF"

    upload_response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("broken.pdf", io.BytesIO(minimal_invalid_pdf), "application/pdf")},
        headers=headers,
    )
    resume_id = upload_response.json()["resume"]["id"]

    response = client.post(f"/api/v1/ats/score/{resume_id}", json={}, headers=headers)
    assert response.status_code == 404


def test_score_for_nonexistent_resume_returns_404():
    token = _register_and_get_token()
    response = client.post(
        "/api/v1/ats/score/does-not-exist", json={}, headers=_auth_headers(token)
    )
    assert response.status_code == 404


def test_users_cannot_score_each_others_resumes():
    token_a = _register_and_get_token()
    token_b = _register_and_get_token()
    resume_id = _upload_resume(_auth_headers(token_a), _STRONG_RESUME_TEXT)

    response = client.post(
        f"/api/v1/ats/score/{resume_id}", json={}, headers=_auth_headers(token_b)
    )
    assert response.status_code == 404


def test_list_reports_returns_history_most_recent_first():
    token = _register_and_get_token()
    headers = _auth_headers(token)
    resume_id = _upload_resume(headers, _STRONG_RESUME_TEXT)

    client.post(f"/api/v1/ats/score/{resume_id}", json={}, headers=headers)
    second = client.post(
        f"/api/v1/ats/score/{resume_id}",
        json={"job_description": _JD_TEXT},
        headers=headers,
    )
    second_report_id = second.json()["id"]

    response = client.get(f"/api/v1/ats/reports/{resume_id}", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    # Most recent (the JD-scored one) should be first.
    assert body["reports"][0]["id"] == second_report_id


def test_list_reports_for_never_scored_resume_returns_empty_list():
    token = _register_and_get_token()
    headers = _auth_headers(token)
    resume_id = _upload_resume(headers, _STRONG_RESUME_TEXT)

    response = client.get(f"/api/v1/ats/reports/{resume_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"total": 0, "reports": []}


def test_get_single_report_returns_full_detail():
    token = _register_and_get_token()
    headers = _auth_headers(token)
    resume_id = _upload_resume(headers, _STRONG_RESUME_TEXT)

    score_response = client.post(
        f"/api/v1/ats/score/{resume_id}",
        json={"job_description": _JD_TEXT},
        headers=headers,
    )
    report_id = score_response.json()["id"]

    response = client.get(f"/api/v1/ats/reports/{resume_id}/{report_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == report_id
    assert response.json()["job_description"] == _JD_TEXT


def test_users_cannot_access_each_others_reports():
    token_a = _register_and_get_token()
    token_b = _register_and_get_token()
    headers_a = _auth_headers(token_a)
    resume_id = _upload_resume(headers_a, _STRONG_RESUME_TEXT)

    score_response = client.post(f"/api/v1/ats/score/{resume_id}", json={}, headers=headers_a)
    report_id = score_response.json()["id"]

    response = client.get(
        f"/api/v1/ats/reports/{resume_id}/{report_id}", headers=_auth_headers(token_b)
    )
    assert response.status_code == 404
