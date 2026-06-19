"""Auth API router — register, login, refresh, logout (bare responses)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from src.application.auth.services.authentication_service import AuthenticationService
from src.presentation.api.dependencies.auth import get_auth_service
from src.presentation.api.v1.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from src.presentation.api.v1.users.schemas import UserData

router = APIRouter(tags=["Authentication"])

AuthServiceDep = Annotated[AuthenticationService, Depends(get_auth_service)]


@router.post(
    "/auth/register",
    response_model=RegisterResponse,
    status_code=201,
    summary="Register a new user account",
    operation_id="registerUser",
)
async def register(body: RegisterRequest, auth: AuthServiceDep) -> RegisterResponse:
    result = await auth.register(
        email=body.email,
        password=body.password,
        display_name=body.display_name,
        phone=body.phone,
    )
    return RegisterResponse(
        id=result.user_id,
        email=result.email,
        display_name=result.display_name,
        created_at=result.created_at,
    )


@router.post(
    "/auth/login",
    response_model=LoginResponse,
    summary="Authenticate with email and password",
    operation_id="login",
)
async def login(body: LoginRequest, auth: AuthServiceDep) -> LoginResponse:
    result = await auth.authenticate(email=body.email, password=body.password)
    return LoginResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        token_type=result.token_type,
        expires_in=result.expires_in,
        user=UserData(
            id=result.user_id,
            email=result.email,
            email_verified=result.email_verified,
            display_name=result.display_name,
            phone=result.phone,
            is_active=result.is_active,
            roles=[],  # populated by GET /users/me immediately after login
            last_login_at=result.last_login_at,
            created_at=result.created_at,
            updated_at=result.updated_at,
        ),
    )


@router.post(
    "/auth/refresh",
    response_model=TokenResponse,
    summary="Rotate tokens using a refresh token",
    operation_id="refreshToken",
)
async def refresh(body: RefreshRequest, auth: AuthServiceDep) -> TokenResponse:
    result = await auth.refresh(refresh_token_value=body.refresh_token)
    return TokenResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        token_type=result.token_type,
        expires_in=result.expires_in,
    )


@router.post(
    "/auth/logout",
    status_code=204,
    summary="Revoke the current refresh token",
    operation_id="logout",
)
async def logout(auth: AuthServiceDep, body: RefreshRequest | None = None) -> None:
    if body is not None and body.refresh_token:
        await auth.logout(refresh_token_value=body.refresh_token)
