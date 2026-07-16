# AI Service API

A production-oriented Python backend built with FastAPI. This project is a
hands-on exercise in software engineering practices for AI services, including
dependency management, automated testing, linting, containerization, and
version control.

## Current capabilities

- Health-check endpoint at `GET /health`
- Interactive OpenAPI documentation at `/docs`
- Automated tests with pytest
- Linting and formatting with Ruff
- Reproducible dependency management with uv
- Non-root Docker container
- Docker Compose health checks

## Prerequisites

- Git
- [uv](https://docs.astral.sh/uv/)
- A Docker-compatible container engine
- Docker Compose

A global Python installation is not required. `uv` installs the Python version
declared in `.python-version` and creates the project environment.

## Local development

Install the locked dependencies:

```bash
uv sync
```

Run the automated checks:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Start the development server:

```bash
uv run uvicorn ai_service_api.main:app --app-dir src --reload
```

The API is then available at:

- API documentation: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/health>

## Running with Docker Compose

If using Colima, start the container engine first:

```bash
colima start
```

Build the image, start the service, and wait for it to become healthy:

```bash
docker compose up --build --wait
```

Inspect the service:

```bash
docker compose ps
docker compose logs api
```

Stop the service and remove its container and network:

```bash
docker compose down
```

## Project structure

```text
.
├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── uv.lock
├── src/
│   └── ai_service_api/
│       ├── __init__.py
│       └── main.py
└── tests/
    └── test_health.py
```

- `pyproject.toml` declares project metadata, dependencies, and tool settings.
- `uv.lock` records the exact resolved dependency versions.
- `src/ai_service_api/` contains production application code.
- `tests/` contains automated behavior checks.
- `Dockerfile` defines the production container image.
- `compose.yaml` defines how the container runs locally.
## Configuration

Application settings use environment variables prefixed with `AI_SERVICE_`.

For local overrides, copy the template:

```bash
cp .env.example .env
```

Supported settings:

| Variable | Default | Description |
| --- | --- | --- |
| `AI_SERVICE_APP_NAME` | `AI Service API` | Name shown in OpenAPI metadata |
| `AI_SERVICE_APP_VERSION` | `0.1.0` | Version shown in OpenAPI metadata |
| `AI_SERVICE_ENVIRONMENT` | `development` | Runtime environment: `development`, `test`, or `production` |

The `.env` file is ignored by Git and Docker. Never commit API keys or other
secrets. Add safe placeholders to `.env.example` when new settings are
introduced.