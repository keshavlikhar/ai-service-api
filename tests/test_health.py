from fastapi.testclient import TestClient

from ai_service_api.config import Settings
from ai_service_api.main import app, create_app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_app_uses_configured_metadata() -> None:
    settings = Settings(
        app_name="Test AI API",
        app_version="9.9.9",
        _env_file=None,
    )
    test_client = TestClient(create_app(settings))

    response = test_client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Test AI API"
    assert response.json()["info"]["version"] == "9.9.9"
