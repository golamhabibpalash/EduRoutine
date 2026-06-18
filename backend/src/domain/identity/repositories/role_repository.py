"""Role repository port."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from src.domain.identity.entities.role import Role


class RoleRepository(Protocol):
    """Persistence contract for the :class:`Role` aggregate."""

    async def get(self, role_id: UUID) -> Role | None:
        """Return the role by id, or ``None``."""
        ...

    async def get_by_name(self, name: str) -> Role | None:
        """Return the role with the given unique name, or ``None``."""
        ...

    async def list(self, *, limit: int, offset: int) -> list[Role]:
        """Return a page of roles."""
        ...

    async def add(self, role: Role) -> None:
        """Stage a new role for persistence."""
        ...

    async def delete(self, role: Role) -> None:
        """Stage a role for removal."""
        ...
