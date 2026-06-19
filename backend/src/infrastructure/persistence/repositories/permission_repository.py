"""SQLAlchemy adapter for :class:`PermissionRepository`."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.entities.permission import Permission
from src.infrastructure.persistence.models.identity import PermissionModel


def _model_to_domain(model: PermissionModel) -> Permission:
    return Permission(
        id=model.id,
        code=model.code,
        name=model.name,
        module=model.module,
        description=model.description,
    )


class SqlAlchemyPermissionRepository:
    """Reads/seeds :class:`Permission` rows via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, permission_id: UUID) -> Permission | None:
        model = await self._session.get(PermissionModel, permission_id)
        return _model_to_domain(model) if model else None

    async def get_by_code(self, code: str) -> Permission | None:
        result = await self._session.execute(
            select(PermissionModel).where(PermissionModel.code == code)
        )
        model = result.scalar_one_or_none()
        return _model_to_domain(model) if model else None

    async def list_page(
        self, *, module: str | None = None, limit: int, offset: int
    ) -> list[Permission]:
        stmt = select(PermissionModel).order_by(PermissionModel.code)
        if module is not None:
            stmt = stmt.where(PermissionModel.module == module)
        stmt = stmt.limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return [_model_to_domain(row) for row in result.scalars()]

    async def count(self, *, module: str | None = None) -> int:
        stmt = select(func.count()).select_from(PermissionModel)
        if module is not None:
            stmt = stmt.where(PermissionModel.module == module)
        result = await self._session.execute(stmt)
        return int(result.scalar_one())

    async def list_by_ids(self, permission_ids: set[UUID]) -> list[Permission]:
        if not permission_ids:
            return []
        result = await self._session.execute(
            select(PermissionModel)
            .where(PermissionModel.id.in_(permission_ids))
            .order_by(PermissionModel.code)
        )
        return [_model_to_domain(row) for row in result.scalars()]

    async def add(self, permission: Permission) -> None:
        self._session.add(
            PermissionModel(
                id=permission.id,
                code=permission.code,
                name=permission.name,
                module=permission.module,
                description=permission.description,
            )
        )
