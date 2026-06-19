"""Aggregate router for API v1."""

from __future__ import annotations

from fastapi import APIRouter

from src.presentation.api.v1.academic.router import router as academic_router
from src.presentation.api.v1.auth.router import router as auth_router
from src.presentation.api.v1.health.router import router as health_router
from src.presentation.api.v1.people.router import router as people_router
from src.presentation.api.v1.periods.router import router as periods_router
from src.presentation.api.v1.routines.router import router as routines_router
from src.presentation.api.v1.roles.router import router as roles_router
from src.presentation.api.v1.rooms.router import router as rooms_router
from src.presentation.api.v1.users.router import router as users_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(roles_router)
api_v1_router.include_router(academic_router)
api_v1_router.include_router(periods_router)
api_v1_router.include_router(routines_router)
api_v1_router.include_router(rooms_router)
api_v1_router.include_router(people_router)
