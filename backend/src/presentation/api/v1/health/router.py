"""Health check endpoint — the only API exposed in Phase 1.

``GET /api/v1/health`` is a public liveness probe (no auth, no DB dependency).
"""

from __future__ import annotations

from fastapi import APIRouter

from src import __version__
from src.presentation.api.common.response_models import SuccessResponse
from src.presentation.api.v1.health.schemas import HealthData
from src.shared.config.settings import get_settings

router = APIRouter(tags=["Authentication"])


@router.get(
    "/health",
    response_model=SuccessResponse[HealthData],
    summary="Liveness/readiness probe",
    operation_id="health",
)
async def health() -> SuccessResponse[HealthData]:
    """Return service liveness. Public; does not touch the database."""
    settings = get_settings()
    return SuccessResponse(
        data=HealthData(
            service=settings.app_name,
            version=__version__,
            environment=settings.app_env,
        )
    )
