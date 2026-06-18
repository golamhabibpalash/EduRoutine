"""Auth API router — register, login, refresh, logout, and user-info endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from src.application.auth.services.authentication_service import (
    AuthenticationService,
    AuthResultDTO,
    TokenPairDTO,
)
from src.presentation.api.dependencies.auth import get_auth_service
from src.presentation.api.v1.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
    RegisterRequest,
    RegisterResponse,
    UserResponse,
)

router = APIRouter(tags=["Authentication"])


@router.post(
    "/auth/register",
    response_model=RegisterResponse,
    summary="Register a new user account",
    operation_id="register",
    status_code=201,
)
async def register(
    body: RegisterRequest,
    auth: AuthenticationService = Depends(get_auth_service),
) -> RegisterResponse:
    result: AuthResultDTO = await auth.register(
        email=body.email,
        password=body.password,
        display_name=body.display_name,
        phone=body.phone,
    )
    return RegisterResponse(
        id=str(result.user_id),
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
async def login(
    body: LoginRequest,
    auth: AuthenticationService = Depends(get_auth_service),
) -> LoginResponse:
    result: AuthResultDTO = await auth.authenticate(email=body.email, password=body.password)
    return LoginResponse(
        access_token=result.access_token,
        refresh_token=result.refresh_token,
        token_type=result.token_type,
        expires_in=result.expires_in,
        user=UserResponse(
            id=str(result.user_id),
            email=result.email,
            email_verified=result.email_verified,
            display_name=result.display_name,
            phone=result.phone,
            is_active=result.is_active,
            status="active" if result.is_active else "suspended",
            last_login_at=result.last_login_at,
            created_at=result.created_at,
            updated_at=result.updated_at,
        ),
    )


@router.post(
    "/auth/refresh",
    response_model=RefreshResponse,
    summary="Refresh access token using a refresh token",
    operation_id="refresh",
)
async def refresh(
    body: RefreshRequest,
    auth: AuthenticationService = Depends(get_auth_service),
) -> RefreshResponse:
    result: TokenPairDTO = await auth.refresh(refresh_token_value=body.refresh_token)
    return RefreshResponse(
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
async def logout(
    body: RefreshRequest | None = None,
    auth: AuthenticationService = Depends(get_auth_service),
) -> None:
    if body is not None and body.refresh_token:
        await auth.logout(refresh_token_value=body.refresh_token)
    return None
