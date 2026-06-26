import io
import uuid

from docx import Document
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# A minimal but real, valid PDF — built so pdfplumber/pypdf can actually
# extract text from it, unlike the magic-bytes-only fixture used in
# test_resumes.py (which is fine for upload validation tests but would
# fail every parsing assertion here).
_REAL_PDF_TEXT = "Jordan Lee\njordan.lee@example.com\n555-123-4567\n\nSkills\nPython, React, AWS, Docker\n\nEducation\nB.Sc. Computer Science, State University, 2022\n\nExperience\nSoftware Engineer at Acme Corp, 2022-Present\n"


def _build_minimal_pdf_bytes(text: str) -> bytes:
    """
    Hand-builds the smallest valid single-page PDF containing the given
    text, using the PDF content-stream Tj operator. Avoids depending on
    a PDF-writing library just for test fixtures.
    """
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


def _build_docx_bytes(text: str) -> bytes:
    document = Document()
    for line in text.split("\n"):
        document.add_paragraph(line)
    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def _register_and_get_token() -> str:
    email = f"parse-test-{uuid.uuid4().hex[:10]}@example.com"
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Parse Tester", "email": email, "password": "supersecret123", "role": "student"},
    )
    return response.json()["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_upload_pdf_returns_parsed_data_automatically():
    token = _register_and_get_token()
    pdf_bytes = _build_minimal_pdf_bytes(_REAL_PDF_TEXT)

    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        headers=_auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()

    assert body["resume"]["file_extension"] == "pdf"
    assert body["parsing_error"] is None
    extracted = body["extracted_data"]
    assert extracted is not None
    assert extracted["email"] == "jordan.lee@example.com"
    assert "python" in extracted["skills"]
    assert "react" in extracted["skills"]
    assert "aws" in extracted["skills"]


def test_upload_docx_returns_parsed_data_automatically():
    token = _register_and_get_token()
    docx_bytes = _build_docx_bytes(_REAL_PDF_TEXT)

    response = client.post(
        "/api/v1/resumes/upload",
        files={
            "file": (
                "resume.docx",
                io.BytesIO(docx_bytes),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
        headers=_auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()
    extracted = body["extracted_data"]
    assert extracted is not None
    assert extracted["email"] == "jordan.lee@example.com"
    assert "docker" in extracted["skills"]


def test_get_parsed_data_endpoint_returns_same_result():
    token = _register_and_get_token()
    headers = _auth_headers(token)
    pdf_bytes = _build_minimal_pdf_bytes(_REAL_PDF_TEXT)

    upload_response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        headers=headers,
    )
    resume_id = upload_response.json()["resume"]["id"]

    response = client.get(f"/api/v1/resumes/{resume_id}/parsed-data", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "jordan.lee@example.com"


def test_get_parsed_data_for_nonexistent_resume_returns_404():
    token = _register_and_get_token()
    response = client.get(
        "/api/v1/resumes/does-not-exist/parsed-data", headers=_auth_headers(token)
    )
    assert response.status_code == 404


def test_users_cannot_access_each_others_parsed_data():
    token_a = _register_and_get_token()
    token_b = _register_and_get_token()
    pdf_bytes = _build_minimal_pdf_bytes(_REAL_PDF_TEXT)

    upload_response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("private.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        headers=_auth_headers(token_a),
    )
    resume_id = upload_response.json()["resume"]["id"]

    response = client.get(
        f"/api/v1/resumes/{resume_id}/parsed-data", headers=_auth_headers(token_b)
    )
    assert response.status_code == 404


def test_reparse_endpoint_returns_fresh_extraction():
    token = _register_and_get_token()
    headers = _auth_headers(token)
    pdf_bytes = _build_minimal_pdf_bytes(_REAL_PDF_TEXT)

    upload_response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("resume.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
        headers=headers,
    )
    resume_id = upload_response.json()["resume"]["id"]

    response = client.post(f"/api/v1/resumes/{resume_id}/reparse", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "jordan.lee@example.com"


def test_upload_with_unparseable_pdf_still_succeeds_with_parsing_error():
    """
    A PDF that passes magic-byte validation (starts with %PDF-) but has
    no real page/text structure should still let the upload succeed —
    only `parsing_error` should be set, per the "don't block storage on
    a parsing limitation" design in api/v1/resumes.py.
    """
    token = _register_and_get_token()
    minimal_invalid_pdf = b"%PDF-1.4\n%%EOF"

    response = client.post(
        "/api/v1/resumes/upload",
        files={"file": ("broken.pdf", io.BytesIO(minimal_invalid_pdf), "application/pdf")},
        headers=_auth_headers(token),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["resume"] is not None
    assert body["extracted_data"] is None
    assert body["parsing_error"] is not None
