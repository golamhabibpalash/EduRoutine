"""User repository port."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from src.domain.identity.entities.user import User
from src.domain.identity.value_objects.email import EmailAddress


class UserRepository(Protocol):
    """Persistence contract for the :class:`User` aggregate."""

    async def get(self, user_id: UUID) -> User | None:
        """Return the user by id, or ``None``."""
        ...

    async def get_by_email(self, email: EmailAddress) -> User | None:
        """Return the active user with the given email, or ``None``."""
        ...

    async def exists_by_email(self, email: EmailAddress) -> bool:
        """Return whether an active user already uses this email."""
        ...

    async def list_page(
        self, *, limit: int, offset: int, is_active: bool | None = None
    ) -> list[User]:
        """Return a page of users, optionally filtered by active status."""
        ...

    async def count(self, *, is_active: bool | None = None) -> int:
        """Return the total number of users matching the filter."""
        ...

    async def add(self, user: User) -> None:
        """Stage a new user for persistence."""
        ...

    async def update(self, user: User) -> None:
        """Persist changes to an existing user."""
        ...

    async def delete(self, user: User) -> None:
        """Stage a user for removal (soft-delete handled by the service layer)."""
        ...

    async def get_role_names(self, user_id: UUID) -> list[str]:
        """Return the names of roles assigned to the user."""
        ...

    async def get_role_ids(self, user_id: UUID) -> set[UUID]:
        """Return the ids of roles assigned to the user."""
        ...

    async def set_role_ids(self, user_id: UUID, role_ids: set[UUID]) -> None:
        """Replace the user's role assignments."""
        ...

    async def get_permission_codes(self, user_id: UUID) -> set[str]:
        """Return the effective permission codes for the user (via their roles)."""
        ...
