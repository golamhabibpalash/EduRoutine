"""Users API router."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends

from src.application.auth.services.authentication_service import (
    AuthenticationService,
    UserInfoDTO,
)
from src.presentation.api.dependencies.auth import get_auth_service, get_current_user_id
from src.presentation.api.v1.auth.schemas import UserResponse

router = APIRouter(tags=["Users"])


@router.get(
    "/users/me",
    response_model=UserResponse,
    summary="Get current user profile",
    operation_id="getMe",
)
async def get_me(
    user_id: UUID = Depends(get_current_user_id),
    auth: AuthenticationService = Depends(get_auth_service),
) -> UserResponse:
    result: UserInfoDTO | None = await auth.get_user_info(user_id)
    return UserResponse(
        id=str(result.id),
        email=result.email,
        email_verified=result.email_verified,
        display_name=result.display_name,
        phone=result.phone,
        status=result.status,
        last_login_at=result.last_login_at,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )
