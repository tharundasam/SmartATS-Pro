from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_app_info():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert "message" in body
    assert body["docs_url"] == "/docs"


def test_health_check_reports_connected_database():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == "connected"
    assert body["app_name"] == "SmartATS Pro API"


def test_openapi_schema_is_available():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "SmartATS Pro API"


def test_swagger_docs_page_loads():
    response = client.get("/docs")
    assert response.status_code == 200
