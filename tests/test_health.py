import logging
from uuid import UUID

import pytest
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


def test_response_includes_valid_request_id() -> None:
    response = client.get("/health")

    request_id = response.headers["x-request-id"]

    assert UUID(request_id).version == 4


def test_each_response_receives_unique_request_id() -> None:
    first_response = client.get("/health")
    second_response = client.get("/health")

    assert (
        first_response.headers["x-request-id"]
        != second_response.headers["x-request-id"]
    )


def test_request_completion_is_logged(
    caplog: pytest.LogCaptureFixture,
) -> None:
    request_logger = logging.getLogger("ai_service_api.requests")
    request_logger.addHandler(caplog.handler)

    try:
        with caplog.at_level(logging.INFO, logger=request_logger.name):
            response = client.get("/health")
    finally:
        request_logger.removeHandler(caplog.handler)

    record = next(
        record for record in caplog.records if record.message == "request_completed"
    )

    assert record.request_id == response.headers["x-request-id"]
    assert record.method == "GET"
    assert record.path == "/health"
    assert record.status_code == 200
    assert record.duration_ms >= 0
