"""Typed application settings loaded from environment / .env (Pydantic Settings)."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application configuration.

    Values are read from environment variables or a local ``.env`` file. See ``.env.example``.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Application
    app_name: str = "EduRoutine"
    app_env: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: str = "postgresql+asyncpg://eduroutine:eduroutine@localhost:5432/eduroutine"
    db_echo: bool = False
    db_pool_size: int = 10
    db_max_overflow: int = 20

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Auth / JWT (base auth only — no social login in Phase 1)
    jwt_algorithm: str = "HS256"
    jwt_secret_key: str = "change-me"  # noqa: S105 — dev default; overridden via env in real envs
    jwt_issuer: str = "eduroutine-api"
    jwt_audience: str = "eduroutine-client"
    access_token_ttl_seconds: int = 900
    refresh_token_ttl_seconds: int = 604800

    # CORS
    cors_allow_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse the comma-separated CORS origins into a list."""
        return [o.strip() for o in self.cors_allow_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance."""
    return Settings()
