"""Permission repository port."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from src.domain.identity.entities.permission import Permission


class PermissionRepository(Protocol):
    """Persistence contract for :class:`Permission` (read-mostly catalog)."""

    async def get(self, permission_id: UUID) -> Permission | None:
        """Return the permission by id, or ``None``."""
        ...

    async def list(self, *, module: str | None = None) -> list[Permission]:
        """Return all permissions, optionally filtered by module."""
        ...
