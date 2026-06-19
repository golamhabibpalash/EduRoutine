"""SQLAlchemy adapter for :class:`RoleRepository`."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.entities.role import Role
from src.infrastructure.persistence.models.identity import RoleModel, RolePermissionModel


def _model_to_domain(model: RoleModel) -> Role:
    return Role(
        id=model.id,
        name=model.name,
        description=model.description,
        is_system_role=model.is_system_role,
        created_at=model.created_at,
    )


class SqlAlchemyRoleRepository:
    """Persists :class:`Role` aggregates via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, role_id: UUID) -> Role | None:
        model = await self._session.get(RoleModel, role_id)
        return _model_to_domain(model) if model else None

    async def get_by_name(self, name: str) -> Role | None:
        result = await self._session.execute(select(RoleModel).where(RoleModel.name == name))
        model = result.scalar_one_or_none()
        return _model_to_domain(model) if model else None

    async def list_page(self, *, limit: int, offset: int) -> list[Role]:
        result = await self._session.execute(
            select(RoleModel).order_by(RoleModel.name).limit(limit).offset(offset)
        )
        return [_model_to_domain(row) for row in result.scalars()]

    async def count(self) -> int:
        result = await self._session.execute(select(func.count()).select_from(RoleModel))
        return int(result.scalar_one())

    async def add(self, role: Role) -> None:
        self._session.add(
            RoleModel(
                id=role.id,
                name=role.name,
                description=role.description,
                is_system_role=role.is_system_role,
            )
        )

    async def update(self, role: Role) -> None:
        model = await self._session.get(RoleModel, role.id)
        if model is None:
            return
        model.name = role.name
        model.description = role.description

    async def delete(self, role: Role) -> None:
        model = await self._session.get(RoleModel, role.id)
        if model:
            await self._session.delete(model)

    async def get_permission_ids(self, role_id: UUID) -> set[UUID]:
        result = await self._session.execute(
            select(RolePermissionModel.permission_id).where(RolePermissionModel.role_id == role_id)
        )
        return set(result.scalars())

    async def set_permission_ids(self, role_id: UUID, permission_ids: set[UUID]) -> None:
        await self._session.execute(
            delete(RolePermissionModel).where(RolePermissionModel.role_id == role_id)
        )
        for permission_id in permission_ids:
            self._session.add(RolePermissionModel(role_id=role_id, permission_id=permission_id))

    async def permission_count(self, role_id: UUID) -> int:
        result = await self._session.execute(
            select(func.count())
            .select_from(RolePermissionModel)
            .where(RolePermissionModel.role_id == role_id)
        )
        return int(result.scalar_one())
