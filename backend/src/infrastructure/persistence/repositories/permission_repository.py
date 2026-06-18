"""SQLAlchemy adapter for :class:`PermissionRepository` (Phase 1 skeleton)."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.entities.permission import Permission


class SqlAlchemyPermissionRepository:
    """Reads :class:`Permission` rows via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, permission_id: UUID) -> Permission | None:
        raise NotImplementedError("SqlAlchemyPermissionRepository.get is a Phase 1 skeleton stub.")

    async def list(self, *, module: str | None = None) -> list[Permission]:
        raise NotImplementedError("SqlAlchemyPermissionRepository.list is a Phase 1 skeleton stub.")
