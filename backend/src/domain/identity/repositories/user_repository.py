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

    async def list(self, *, limit: int, offset: int) -> list[User]:
        """Return a page of users."""
        ...

    async def add(self, user: User) -> None:
        """Stage a new user for persistence."""
        ...

    async def delete(self, user: User) -> None:
        """Stage a user for removal (soft-delete handled by the service layer)."""
        ...
