import pytest

from ai_service_api.config import Settings


def test_settings_use_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_name == "AI Service API"
    assert settings.app_version == "0.1.0"
    assert settings.environment == "development"


def test_settings_read_prefixed_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AI_SERVICE_ENVIRONMENT", "production")

    settings = Settings(_env_file=None)

    assert settings.environment == "production"
