"""User aggregate root."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.domain.common.entity import AggregateRoot
from src.domain.identity.value_objects.email import EmailAddress


@dataclass(eq=False)
class User(AggregateRoot):
    """A system user account (aggregate root of the identity context).

    Mirrors ``identity.users`` (docs/03-database-design.md). Behavior is intentionally minimal in
    the Phase 1 skeleton; invariants/state transitions are added in later phases.
    """

    email: EmailAddress
    password_hash: str
    display_name: str
    email_verified: bool = False
    phone: str | None = None
    is_active: bool = True
    last_login_at: datetime | None = None
    role_ids: set[UUID] = field(default_factory=set)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def deactivate(self) -> None:
        """Soft-deactivate the account."""
        self.is_active = False

    def assign_role(self, role_id: UUID) -> None:
        """Grant a role to the user (idempotent)."""
        self.role_ids.add(role_id)
