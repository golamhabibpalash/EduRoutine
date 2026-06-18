"""SQLAlchemy adapter for :class:`UserRepository`."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.identity.entities.user import User
from src.domain.identity.value_objects.email import EmailAddress
from src.infrastructure.persistence.models.identity import UserModel


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
            select(UserModel.id).where(UserModel.email == email.value, UserModel.is_active.is_(True))
        )
        return result.scalar() is not None

    async def list(self, *, limit: int, offset: int) -> list[User]:
        result = await self._session.execute(
            select(UserModel).order_by(UserModel.created_at).limit(limit).offset(offset)
        )
        return [_model_to_domain(row) for row in result.scalars()]

    async def add(self, user: User) -> None:
        model = _domain_to_model(user)
        self._session.add(model)

    async def delete(self, user: User) -> None:
        model = await self._session.get(UserModel, user.id)
        if model:
            await self._session.delete(model)
