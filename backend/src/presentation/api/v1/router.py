"""Aggregate router for API v1.

Phase 1 exposes only the health check. Business module routers (auth, users, roles, ...) are
registered here as they are implemented in later phases.
"""

from __future__ import annotations

from fastapi import APIRouter

from src.presentation.api.v1.health.router import router as health_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
