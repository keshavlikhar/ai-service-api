from fastapi import FastAPI

from ai_service_api.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or Settings()

    application = FastAPI(
        title=app_settings.app_name,
        version=app_settings.app_version,
    )

    @application.get("/health", tags=["health"])
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return application


app = create_app()
