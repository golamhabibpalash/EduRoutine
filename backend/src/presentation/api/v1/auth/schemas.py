"""Auth endpoint request/response Pydantic schemas."""

from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: str = Field(..., examples=["admin@eduroutine.com"])
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class UserResponse(BaseModel):
    id: str
    email: str
    email_verified: bool
    display_name: str
    phone: str | None = None
    status: str
    last_login_at: str | None = None
    created_at: str
    updated_at: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user: UserResponse


class RegisterRequest(BaseModel):
    email: str = Field(..., examples=["admin@eduroutine.com"])
    password: str = Field(..., min_length=6)
    display_name: str = Field(..., min_length=1, max_length=200)
    phone: str | None = Field(None, max_length=30)


class RegisterResponse(BaseModel):
    id: str
    email: str
    display_name: str
    created_at: str


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
