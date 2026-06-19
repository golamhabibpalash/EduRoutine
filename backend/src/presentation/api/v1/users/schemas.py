"""User & claim request/response schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.application.users.dto import ClaimDTO, UserDTO


class UserData(BaseModel):
    """User response payload (envelope ``data``)."""

    id: UUID
    email: str
    email_verified: bool
    display_name: str
    phone: str | None
    is_active: bool
    roles: list[str]
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, dto: UserDTO) -> UserData:
        return cls(
            id=dto.id,
            email=dto.email,
            email_verified=dto.email_verified,
            display_name=dto.display_name,
            phone=dto.phone,
            is_active=dto.is_active,
            roles=list(dto.roles),
            last_login_at=dto.last_login_at,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )


class ClaimData(BaseModel):
    """Claim response payload."""

    id: UUID
    user_id: UUID
    claim_type: str
    claim_value: str

    @classmethod
    def from_dto(cls, dto: ClaimDTO) -> ClaimData:
        return cls(
            id=dto.id, user_id=dto.user_id, claim_type=dto.claim_type, claim_value=dto.claim_value
        )


class CreateUserRequest(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(min_length=12, max_length=128)
    display_name: str = Field(min_length=2, max_length=200)
    phone: str | None = Field(default=None, max_length=30)
    is_active: bool = True
    role_ids: list[UUID] = Field(default_factory=list)


class UpdateUserRequest(BaseModel):
    """PATCH /users/{id} — all fields optional."""

    display_name: str | None = Field(default=None, min_length=2, max_length=200)
    phone: str | None = Field(default=None, max_length=30)
    is_active: bool | None = None


class ReplaceUserRequest(BaseModel):
    """PUT /users/{id}."""

    display_name: str = Field(min_length=2, max_length=200)
    phone: str | None = Field(default=None, max_length=30)
    is_active: bool


class UpdateProfileRequest(BaseModel):
    """PATCH /users/me."""

    display_name: str | None = Field(default=None, min_length=2, max_length=200)
    phone: str | None = Field(default=None, max_length=30)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=12, max_length=128)


class SetUserRolesRequest(BaseModel):
    role_ids: list[UUID]


class CreateClaimRequest(BaseModel):
    claim_type: str = Field(min_length=1, max_length=200)
    claim_value: str = Field(min_length=1, max_length=500)
