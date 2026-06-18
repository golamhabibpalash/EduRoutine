"""FastAPI application entrypoint (Phase 1 skeleton).

Exposes only ``GET /api/v1/health``. Wires CORS, correlation-id middleware, and the standard
exception handlers. Business routers are added in later phases.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import __version__
from src.presentation.api.common.error_handlers import register_exception_handlers
from src.presentation.api.middleware.correlation_id import CorrelationIdMiddleware
from src.presentation.api.v1.router import api_v1_router
from src.shared.config.settings import get_settings


def create_app() -> FastAPI:
    """Application factory."""
    settings = get_settings()

    app = FastAPI(
        title=f"{settings.app_name} API",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
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
