import uuid

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _unique_email() -> str:
    return f"test-{uuid.uuid4().hex[:10]}@example.com"


def test_register_returns_token_and_user():
    email = _unique_email()
    response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Test Student", "email": email, "password": "supersecret123", "role": "student"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["user"]["email"] == email
    assert body["user"]["role"] == "student"
    assert "access_token" in body


def test_register_duplicate_email_returns_409():
    email = _unique_email()
    payload = {"full_name": "Dup", "email": email, "password": "supersecret123", "role": "student"}
    first = client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 409


def test_login_json_with_correct_credentials_succeeds():
    email = _unique_email()
    client.post(
        "/api/v1/auth/register",
        json={"full_name": "Login Test", "email": email, "password": "supersecret123", "role": "student"},
    )

    response = client.post(
        "/api/v1/auth/login/json",
        json={"email": email, "password": "supersecret123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_json_with_wrong_password_returns_401():
    email = _unique_email()
    client.post(
        "/api/v1/auth/register",
        json={"full_name": "Wrong Pass", "email": email, "password": "supersecret123", "role": "student"},
    )

    response = client.post(
        "/api/v1/auth/login/json",
        json={"email": email, "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_login_oauth2_form_succeeds():
    email = _unique_email()
    client.post(
        "/api/v1/auth/register",
        json={"full_name": "Form Login", "email": email, "password": "supersecret123", "role": "student"},
    )

    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "supersecret123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_me_requires_valid_token():
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401  # no Authorization header at all


def test_me_returns_current_user_with_valid_token():
    email = _unique_email()
    register_response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Me Test", "email": email, "password": "supersecret123", "role": "student"},
    )
    token = register_response.json()["access_token"]

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == email


def test_student_cannot_access_placement_officer_route():
    email = _unique_email()
    register_response = client.post(
        "/api/v1/auth/register",
        json={"full_name": "Student User", "email": email, "password": "supersecret123", "role": "student"},
    )
    token = register_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/placement-officer-check", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_placement_officer_can_access_placement_officer_route():
    email = _unique_email()
    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Officer User",
            "email": email,
            "password": "supersecret123",
            "role": "placement_officer",
        },
    )
    token = register_response.json()["access_token"]

    response = client.get(
        "/api/v1/auth/placement-officer-check", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Placement Officer access" in response.json()["message"]
