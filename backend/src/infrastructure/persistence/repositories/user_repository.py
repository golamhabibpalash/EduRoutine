"""SQLAlchemy adapter for :class:`UserRepository` (Phase 1 skeleton)."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.entities.user import User
from src.domain.identity.value_objects.email import EmailAddress


class SqlAlchemyUserRepository:
    """Persists :class:`User` aggregates via SQLAlchemy.

    Method bodies are stubs in Phase 1; ORM⇄domain mapping is implemented in a later phase.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, user_id: UUID) -> User | None:
        raise NotImplementedError("SqlAlchemyUserRepository.get is a Phase 1 skeleton stub.")

    async def get_by_email(self, email: EmailAddress) -> User | None:
        raise NotImplementedError(
            "SqlAlchemyUserRepository.get_by_email is a Phase 1 skeleton stub."
        )

    async def exists_by_email(self, email: EmailAddress) -> bool:
        raise NotImplementedError(
            "SqlAlchemyUserRepository.exists_by_email is a Phase 1 skeleton stub."
        )

    async def list(self, *, limit: int, offset: int) -> list[User]:
        raise NotImplementedError("SqlAlchemyUserRepository.list is a Phase 1 skeleton stub.")

    async def add(self, user: User) -> None:
        raise NotImplementedError("SqlAlchemyUserRepository.add is a Phase 1 skeleton stub.")

    async def delete(self, user: User) -> None:
        raise NotImplementedError("SqlAlchemyUserRepository.delete is a Phase 1 skeleton stub.")
