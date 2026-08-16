import json
import logging

from ai_service_api.logging_config import JsonFormatter, configure_logging


def test_json_formatter_serializes_request_metadata() -> None:
    record = logging.LogRecord(
        name="ai_service_api.requests",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="request_completed",
        args=(),
        exc_info=None,
    )
    record.request_id = "test-request-id"
    record.method = "GET"
    record.path = "/health"
    record.status_code = 200
    record.duration_ms = 12.5

    payload = json.loads(JsonFormatter().format(record))

    assert payload["level"] == "INFO"
    assert payload["logger"] == "ai_service_api.requests"
    assert payload["event"] == "request_completed"
    assert payload["request_id"] == "test-request-id"
    assert payload["method"] == "GET"
    assert payload["path"] == "/health"
    assert payload["status_code"] == 200
    assert payload["duration_ms"] == 12.5
    assert isinstance(payload["timestamp"], str)


def test_configure_logging_installs_json_handler() -> None:
    application_logger = logging.getLogger("ai_service_api")

    original_handlers = application_logger.handlers.copy()
    original_level = application_logger.level
    original_propagate = application_logger.propagate

    try:
        configure_logging()

        assert application_logger.level == logging.INFO
        assert application_logger.propagate is False
        assert len(application_logger.handlers) == 1
        assert isinstance(
            application_logger.handlers[0].formatter,
            JsonFormatter,
        )
    finally:
        application_logger.handlers[:] = original_handlers
        application_logger.setLevel(original_level)
        application_logger.propagate = original_propagate
