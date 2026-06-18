"""FastAPI application entrypoint."""

from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import __version__
from src.presentation.api.common.error_handlers import register_exception_handlers
from src.presentation.api.middleware.correlation_id import CorrelationIdMiddleware
from src.presentation.api.v1.router import api_v1_router
from src.shared.config.settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan — runs seed on startup in development mode."""
    settings = get_settings()
    if settings.app_env == "development":
        try:
            from src.application.auth.seed import seed_admin_user  # noqa: PLC0415
            await seed_admin_user()
        except Exception:
            pass  # non-blocking — app continues even if seed fails
    yield


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()

    app = FastAPI(
        title=f"{settings.app_name} API",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)
    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
