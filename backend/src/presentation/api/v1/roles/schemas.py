"""Role & permission request/response schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.application.roles.dto import PermissionDTO, RoleDTO


class RoleData(BaseModel):
    """Role response payload (envelope ``data``)."""

    id: UUID
    name: str
    description: str | None
    is_system_role: bool
    permission_count: int
    created_at: datetime

    @classmethod
    def from_dto(cls, dto: RoleDTO) -> RoleData:
        return cls(
            id=dto.id,
            name=dto.name,
            description=dto.description,
            is_system_role=dto.is_system_role,
            permission_count=dto.permission_count,
            created_at=dto.created_at,
        )


class PermissionData(BaseModel):
    """Permission response payload."""

    id: UUID
    code: str
    name: str
    module: str
    description: str | None

    @classmethod
    def from_dto(cls, dto: PermissionDTO) -> PermissionData:
        return cls(
            id=dto.id, code=dto.code, name=dto.name, module=dto.module, description=dto.description
        )


class CreateRoleRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100, pattern=r"^[a-z][a-z0-9_]*$")
    description: str | None = Field(default=None, max_length=500)
    permission_ids: list[UUID] = Field(default_factory=list)


class UpdateRoleRequest(BaseModel):
    name: str | None = Field(
        default=None, min_length=2, max_length=100, pattern=r"^[a-z][a-z0-9_]*$"
    )
    description: str | None = Field(default=None, max_length=500)


class SetRolePermissionsRequest(BaseModel):
    permission_ids: list[UUID]
