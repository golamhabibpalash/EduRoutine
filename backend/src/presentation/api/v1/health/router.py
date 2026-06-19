"""Health check endpoint (public, bare response)."""

from __future__ import annotations

from fastapi import APIRouter

from src import __version__
from src.presentation.api.v1.health.schemas import HealthData
from src.shared.config.settings import get_settings

router = APIRouter(tags=["Authentication"])


@router.get("/health", response_model=HealthData, summary="Liveness probe", operation_id="health")
async def health() -> HealthData:
    """Return service liveness. Public; does not touch the database."""
    settings = get_settings()
    return HealthData(
        status="ok",
        service=settings.app_name,
        version=__version__,
        environment=settings.app_env,
    )
