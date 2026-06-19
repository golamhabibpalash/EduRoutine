"""SQLAlchemy adapter for :class:`UserRepository`."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.entities.user import User
from src.domain.identity.value_objects.email import EmailAddress
from src.infrastructure.persistence.models.identity import (
    PermissionModel,
    RoleModel,
    RolePermissionModel,
    UserModel,
    UserRoleModel,
)


def _model_to_domain(model: UserModel) -> User:
    return User(
        id=model.id,
        email=EmailAddress(model.email),
        password_hash=model.password_hash,
        display_name=model.display_name,
        email_verified=model.email_verified,
        phone=model.phone,
        is_active=model.is_active,
        last_login_at=model.last_login_at,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _domain_to_model(user: User) -> UserModel:
    return UserModel(
        id=user.id,
        email=user.email.value,
        password_hash=user.password_hash,
        display_name=user.display_name,
        email_verified=user.email_verified,
        phone=user.phone,
        is_active=user.is_active,
        last_login_at=user.last_login_at,
    )


class SqlAlchemyUserRepository:
    """Persists :class:`User` aggregates via SQLAlchemy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, user_id: UUID) -> User | None:
        result = await self._session.get(UserModel, user_id)
        return _model_to_domain(result) if result else None

    async def get_by_email(self, email: EmailAddress) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.value, UserModel.is_active.is_(True))
        )
        row = result.scalar_one_or_none()
        return _model_to_domain(row) if row else None

    async def exists_by_email(self, email: EmailAddress) -> bool:
        result = await self._session.execute(
            select(UserModel.id).where(
                UserModel.email == email.value, UserModel.is_active.is_(True)
            )
        )
        return result.scalar() is not None

    async def list_page(
        self, *, limit: int, offset: int, is_active: bool | None = None
    ) -> list[User]:
        stmt = select(UserModel).order_by(UserModel.created_at.desc())
        if is_active is not None:
            stmt = stmt.where(UserModel.is_active.is_(is_active))
        stmt = stmt.limit(limit).offset(offset)
        result = await self._session.execute(stmt)
        return [_model_to_domain(row) for row in result.scalars()]

    async def count(self, *, is_active: bool | None = None) -> int:
        stmt = select(func.count()).select_from(UserModel)
        if is_active is not None:
            stmt = stmt.where(UserModel.is_active.is_(is_active))
        result = await self._session.execute(stmt)
        return int(result.scalar_one())

    async def add(self, user: User) -> None:
        self._session.add(_domain_to_model(user))

    async def update(self, user: User) -> None:
        model = await self._session.get(UserModel, user.id)
        if model is None:
            return
        model.email = user.email.value
        model.password_hash = user.password_hash
        model.display_name = user.display_name
        model.email_verified = user.email_verified
        model.phone = user.phone
        model.is_active = user.is_active
        model.last_login_at = user.last_login_at

    async def delete(self, user: User) -> None:
        model = await self._session.get(UserModel, user.id)
        if model:
            await self._session.delete(model)

    async def get_role_names(self, user_id: UUID) -> list[str]:
        result = await self._session.execute(
            select(RoleModel.name)
            .join(UserRoleModel, UserRoleModel.role_id == RoleModel.id)
            .where(UserRoleModel.user_id == user_id)
            .order_by(RoleModel.name)
        )
        return list(result.scalars())

    async def get_role_ids(self, user_id: UUID) -> set[UUID]:
        result = await self._session.execute(
            select(UserRoleModel.role_id).where(UserRoleModel.user_id == user_id)
        )
        return set(result.scalars())

    async def set_role_ids(self, user_id: UUID, role_ids: set[UUID]) -> None:
        await self._session.execute(delete(UserRoleModel).where(UserRoleModel.user_id == user_id))
        for role_id in role_ids:
            self._session.add(UserRoleModel(user_id=user_id, role_id=role_id))

    async def get_permission_codes(self, user_id: UUID) -> set[str]:
        result = await self._session.execute(
            select(PermissionModel.code)
            .join(
                RolePermissionModel,
                RolePermissionModel.permission_id == PermissionModel.id,
            )
            .join(UserRoleModel, UserRoleModel.role_id == RolePermissionModel.role_id)
            .where(UserRoleModel.user_id == user_id)
        )
        return set(result.scalars())
