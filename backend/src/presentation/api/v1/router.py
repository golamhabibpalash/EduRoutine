"""Aggregate router for API v1."""

from __future__ import annotations

from fastapi import APIRouter

from src.presentation.api.v1.auth.router import router as auth_router
from src.presentation.api.v1.health.router import router as health_router
from src.presentation.api.v1.users.router import router as users_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
