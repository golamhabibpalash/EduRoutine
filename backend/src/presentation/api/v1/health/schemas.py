"""Health endpoint response schema."""

from __future__ import annotations

from pydantic import BaseModel


class HealthData(BaseModel):
    """Liveness payload returned by ``GET /api/v1/health``."""

    status: str = "ok"
    service: str
    version: str
    environment: str
