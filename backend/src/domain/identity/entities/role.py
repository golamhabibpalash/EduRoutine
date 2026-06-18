"""Role aggregate root."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Role(AggregateRoot):
    """A named collection of permissions (RBAC). Mirrors ``identity.roles``."""

    name: str
    description: str | None = None
    is_system_role: bool = False
    permission_ids: set[UUID] = field(default_factory=set)
    created_at: datetime | None = None

    def grant(self, permission_id: UUID) -> None:
        """Add a permission to the role (idempotent)."""
        self.permission_ids.add(permission_id)

    def revoke(self, permission_id: UUID) -> None:
        """Remove a permission from the role if present."""
        self.permission_ids.discard(permission_id)
