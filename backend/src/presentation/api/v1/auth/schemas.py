"""Auth endpoint request/response schemas (bare shapes)."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.presentation.api.v1.users.schemas import UserData


class RegisterRequest(BaseModel):
    email: str = Field(max_length=255, examples=["user@eduroutine.com"])
    password: str = Field(min_length=12, max_length=128)
    display_name: str = Field(min_length=2, max_length=200)
    phone: str | None = Field(default=None, max_length=30)


class LoginRequest(BaseModel):
    email: str = Field(examples=["admin@eduroutine.com"])
    password: str = Field(min_length=1)


class RefreshRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: str = Field(max_length=255)


class ResetPasswordRequest(BaseModel):
    # Field name matches the frontend payload (`{ token, password }`).
    token: str
    password: str = Field(min_length=12, max_length=128)


class TokenResponse(BaseModel):
    """Refresh response: tokens only."""

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"  # noqa: S105 — field name, not a secret
    expires_in: int


class LoginResponse(BaseModel):
    """Login response: tokens + embedded user."""

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"  # noqa: S105 — field name, not a secret
    expires_in: int
    user: UserData


class RegisterResponse(BaseModel):
    id: UUID
    email: str
    display_name: str
    created_at: datetime
