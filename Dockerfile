FROM python:3.13.14-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.11.29 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN useradd --create-home --uid 10001 appuser

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

COPY src ./src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src"

USER appuser

EXPOSE 8000

CMD ["uvicorn", "ai_service_api.main:app", "--host", "0.0.0.0", "--port", "8000"]