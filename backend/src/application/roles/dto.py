"""Role/permission read-model DTOs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class RoleDTO:
    """Read model for a role, mapped to ``RoleResponse``."""

    id: UUID
    name: str
    description: str | None
    is_system_role: bool
    permission_count: int
    created_at: datetime


@dataclass(frozen=True)
class PermissionDTO:
    """Read model for a permission, mapped to ``PermissionResponse``."""

    id: UUID
    code: str
    name: str
    module: str
    description: str | None
