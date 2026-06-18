"""Unit of Work port — transactional boundary exposing repositories."""

from __future__ import annotations

from types import TracebackType
from typing import Protocol, runtime_checkable

from src.domain.identity.repositories import (
    ClaimRepository,
    PermissionRepository,
    RoleRepository,
    UserRepository,
)


@runtime_checkable
class UnitOfWork(Protocol):
    """Atomic transaction boundary that aggregates the identity repositories.

    Command handlers depend on this port; the infrastructure layer provides the SQLAlchemy
    implementation. Use as an async context manager:

        async with uow:
            await uow.users.add(user)
            await uow.commit()
    """

    users: UserRepository
    roles: RoleRepository
    permissions: PermissionRepository
    claims: ClaimRepository

    async def __aenter__(self) -> UnitOfWork:
        """Begin a transaction."""
        ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """Roll back on error; release resources."""
        ...

    async def commit(self) -> None:
        """Persist all staged changes."""
        ...

    async def rollback(self) -> None:
        """Discard all staged changes."""
        ...
