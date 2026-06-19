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

    async def get_by_code(self, code: str) -> Permission | None:
        """Return the permission with the given unique code, or ``None``."""
        ...

    async def list_page(
        self, *, module: str | None = None, limit: int, offset: int
    ) -> list[Permission]:
        """Return a page of permissions, optionally filtered by module."""
        ...

    async def count(self, *, module: str | None = None) -> int:
        """Return the total number of permissions matching the filter."""
        ...

    async def list_by_ids(self, permission_ids: set[UUID]) -> list[Permission]:
        """Return permissions whose ids are in ``permission_ids``."""
        ...

    async def add(self, permission: Permission) -> None:
        """Stage a new permission for persistence (catalog seeding)."""
        ...
