"""SQLAlchemy adapter for :class:`RoleRepository` (Phase 1 skeleton)."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.entities.role import Role


class SqlAlchemyRoleRepository:
    """Persists :class:`Role` aggregates via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, role_id: UUID) -> Role | None:
        raise NotImplementedError("SqlAlchemyRoleRepository.get is a Phase 1 skeleton stub.")

    async def get_by_name(self, name: str) -> Role | None:
        raise NotImplementedError(
            "SqlAlchemyRoleRepository.get_by_name is a Phase 1 skeleton stub."
        )

    async def list(self, *, limit: int, offset: int) -> list[Role]:
        raise NotImplementedError("SqlAlchemyRoleRepository.list is a Phase 1 skeleton stub.")

    async def add(self, role: Role) -> None:
        raise NotImplementedError("SqlAlchemyRoleRepository.add is a Phase 1 skeleton stub.")

    async def delete(self, role: Role) -> None:
        raise NotImplementedError("SqlAlchemyRoleRepository.delete is a Phase 1 skeleton stub.")
