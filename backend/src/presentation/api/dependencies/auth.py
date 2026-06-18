"""Auth service and JWT dependencies."""

from __future__ import annotations

from collections.abc import AsyncIterator
from uuid import UUID

from fastapi import Depends, Header

import jwt
from jwt.exceptions import PyJWTError

from src.application.auth.services.authentication_service import AuthenticationService
from src.infrastructure.auth.jwt_service import JWTService
from src.infrastructure.auth.password_hasher import Argon2PasswordHasher
from src.infrastructure.auth.refresh_token_service import RefreshTokenService
from src.infrastructure.persistence.database import get_sessionmaker
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.shared.config.settings import get_settings


async def get_auth_service() -> AsyncIterator[AuthenticationService]:
    """Yield an :class:`AuthenticationService` wired with infrastructure adapters.

    The UnitOfWork is entered here (request scope) so the same session is reused across
    service calls — the service itself must NOT call ``async with self._uow`` again.
    """
    settings = get_settings()
    session_factory = get_sessionmaker()
    async with SqlAlchemyUnitOfWork(session_factory) as uow:
        password_hasher = Argon2PasswordHasher()
        jwt_service = JWTService(settings)
        refresh_token_service = RefreshTokenService(uow.session)
        yield AuthenticationService(
            uow=uow,
            password_hasher=password_hasher,
            jwt_service=jwt_service,
            refresh_token_service=refresh_token_service,
        )


async def get_current_user_id(
    authorization: str = Header(..., alias="Authorization"),
) -> UUID:
    """Extract and validate the current user ID from the Bearer JWT."""
    settings = get_settings()
    if not authorization.startswith("Bearer "):
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.removeprefix("Bearer ")
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
        )
    except PyJWTError:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("sub")
    if user_id is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return UUID(user_id)
