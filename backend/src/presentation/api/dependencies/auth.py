"""Authentication & authorization dependencies."""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, Header, HTTPException
from jwt.exceptions import PyJWTError

from src.application.auth.services.authentication_service import AuthenticationService
from src.application.common.exceptions import PermissionDeniedError
from src.infrastructure.auth.jwt_service import JWTService
from src.infrastructure.auth.password_hasher import Argon2PasswordHasher
from src.infrastructure.auth.password_reset_service import PasswordResetService
from src.infrastructure.auth.refresh_token_service import RefreshTokenService
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork
from src.shared.config.settings import get_settings

SUPER_ADMIN_ROLE = "super_admin"


async def get_auth_service() -> AsyncIterator[AuthenticationService]:
    """Yield an :class:`AuthenticationService` wired with infrastructure adapters."""
    settings = get_settings()
    async with SqlAlchemyUnitOfWork() as uow:
        yield AuthenticationService(
            uow=uow,
            password_hasher=Argon2PasswordHasher(),
            jwt_service=JWTService(settings),
            refresh_token_service=RefreshTokenService(uow.session),
            password_reset_service=PasswordResetService(uow.session),
        )


async def get_current_user_id(
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> UUID:
    """Extract and validate the current user id from the Bearer JWT."""
    settings = get_settings()
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header.")

    token = authorization.removeprefix("Bearer ")
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
        )
    except PyJWTError as err:
        raise HTTPException(status_code=401, detail="Invalid or expired token.") from err

    subject = payload.get("sub")
    if subject is None:
        raise HTTPException(status_code=401, detail="Invalid token payload.")
    return UUID(subject)


@dataclass(frozen=True)
class Principal:
    """The authenticated caller plus their effective roles and permissions."""

    user_id: UUID
    roles: frozenset[str]
    permissions: frozenset[str]

    def has_permission(self, code: str) -> bool:
        return SUPER_ADMIN_ROLE in self.roles or code in self.permissions


async def get_current_principal(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
) -> Principal:
    """Load the caller's roles and effective permission codes."""
    async with SqlAlchemyUnitOfWork() as uow:
        user = await uow.users.get(user_id)
        if user is None or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found or inactive.")
        roles = frozenset(await uow.users.get_role_names(user_id))
        permissions = frozenset(await uow.users.get_permission_codes(user_id))
    return Principal(user_id=user_id, roles=roles, permissions=permissions)


def require_permission(code: str) -> Callable[[Principal], Awaitable[Principal]]:
    """Build a dependency that authorizes the caller for ``code`` (super_admin bypasses)."""

    async def _dependency(
        principal: Annotated[Principal, Depends(get_current_principal)],
    ) -> Principal:
        if not principal.has_permission(code):
            raise PermissionDeniedError(f"Missing required permission: {code}")
        return principal

    return _dependency


CurrentUserId = Annotated[UUID, Depends(get_current_user_id)]
CurrentPrincipal = Annotated[Principal, Depends(get_current_principal)]
