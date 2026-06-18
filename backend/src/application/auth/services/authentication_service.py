"""Authentication application service."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.application.common.exceptions import AuthenticationError, ConflictError
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.domain.identity.entities.user import User
from src.domain.identity.services import PasswordHasher
from src.domain.identity.value_objects.email import EmailAddress
from src.infrastructure.auth.jwt_service import JWTService
from src.infrastructure.auth.refresh_token_service import RefreshTokenService
from src.shared.config.settings import get_settings
from src.shared.utils.clock import utcnow


@dataclass(frozen=True)
class TokenPairDTO:
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = field(default_factory=lambda: get_settings().access_token_ttl_seconds)


@dataclass(frozen=True)
class AuthResultDTO:
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    user_id: UUID
    email: str
    display_name: str
    email_verified: bool
    phone: str | None
    is_active: bool
    last_login_at: str | None
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class UserInfoDTO:
    id: UUID
    email: str
    email_verified: bool
    display_name: str
    phone: str | None
    status: str
    last_login_at: str | None
    created_at: str
    updated_at: str


class AuthenticationService:
    """Coordinates credential verification and token issuance."""

    def __init__(
        self,
        uow: UnitOfWork,
        password_hasher: PasswordHasher,
        jwt_service: JWTService,
        refresh_token_service: RefreshTokenService,
    ) -> None:
        self._uow = uow
        self._hasher = password_hasher
        self._jwt = jwt_service
        self._refresh = refresh_token_service

    async def register(self, email: str, password: str, display_name: str, phone: str | None = None) -> AuthResultDTO:
        email_vo = EmailAddress(email)
        exists = await self._uow.users.exists_by_email(email_vo)
        if exists:
            raise ConflictError("A user with this email already exists.")

        password_hash = self._hasher.hash(password)
        now = utcnow()
        user = User(
            id=uuid4(),
            email=email_vo,
            password_hash=password_hash,
            display_name=display_name,
            phone=phone,
            created_at=now,
            updated_at=now,
        )
        await self._uow.users.add(user)
        access_token = self._jwt.issue_access_token(subject=str(user.id), claims={"email": email})
        refresh_token = await self._refresh.create(user.id)
        await self._uow.commit()

        return self._build_auth_result(user, access_token, refresh_token)

    async def authenticate(self, email: str, password: str) -> AuthResultDTO:
        email_vo = EmailAddress(email)
        user = await self._uow.users.get_by_email(email_vo)
        if user is None:
            raise AuthenticationError("Invalid email or password.")

        if not self._hasher.verify(password, user.password_hash):
            raise AuthenticationError("Invalid email or password.")

        if not user.is_active:
            raise AuthenticationError("Account is deactivated.")

        user.last_login_at = utcnow()
        access_token = self._jwt.issue_access_token(subject=str(user.id), claims={"email": email})
        refresh_token = await self._refresh.create(user.id)
        await self._uow.commit()

        return self._build_auth_result(user, access_token, refresh_token)

    async def refresh(self, refresh_token_value: str) -> TokenPairDTO:
        user_id = await self._refresh.consume(refresh_token_value)
        access_token = self._jwt.issue_access_token(subject=str(user_id))
        new_refresh_token = await self._refresh.create(user_id)
        await self._uow.commit()

        settings = get_settings()
        return TokenPairDTO(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=settings.access_token_ttl_seconds,
        )

    async def logout(self, refresh_token_value: str) -> None:
        await self._refresh.revoke(refresh_token_value)
        await self._uow.commit()

    async def get_user_info(self, user_id: UUID) -> UserInfoDTO | None:
        user = await self._uow.users.get(user_id)
        if user is None:
            return None
        return self._build_user_info(user)

    def _build_auth_result(self, user: User, access_token: str, refresh_token: str) -> AuthResultDTO:
        settings = get_settings()
        return AuthResultDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=settings.access_token_ttl_seconds,
            user_id=user.id,
            email=user.email.value,
            display_name=user.display_name,
            email_verified=user.email_verified,
            phone=user.phone,
            is_active=user.is_active,
            last_login_at=user.last_login_at.isoformat() if user.last_login_at else None,
            created_at=user.created_at.isoformat() if user.created_at else "",
            updated_at=user.updated_at.isoformat() if user.updated_at else "",
        )

    def _build_user_info(self, user: User) -> UserInfoDTO:
        status = "suspended" if not user.is_active else "active"
        return UserInfoDTO(
            id=user.id,
            email=user.email.value,
            email_verified=user.email_verified,
            display_name=user.display_name,
            phone=user.phone,
            status=status,
            last_login_at=user.last_login_at.isoformat() if user.last_login_at else None,
            created_at=user.created_at.isoformat() if user.created_at else "",
            updated_at=user.updated_at.isoformat() if user.updated_at else "",
        )
