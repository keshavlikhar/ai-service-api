from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AI_SERVICE_",
        extra="ignore",
    )

    app_name: str = "AI Service API"
    app_version: str = "0.1.0"
    environment: Literal["development", "test", "production"] = "development"
