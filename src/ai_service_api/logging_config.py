import json
import logging
from datetime import UTC, datetime

REQUEST_LOG_FIELDS = (
    "request_id",
    "method",
    "path",
    "status_code",
    "duration_ms",
)

APPLICATION_LOGGER_NAME = "ai_service_api"


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
        }

        for field in REQUEST_LOG_FIELDS:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value

        if record.exc_info is not None:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )


def configure_logging() -> None:
    application_logger = logging.getLogger(APPLICATION_LOGGER_NAME)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    application_logger.handlers.clear()
    application_logger.addHandler(handler)
    application_logger.setLevel(logging.INFO)
    application_logger.propagate = False
