"""Refresh token service — stores, validates, and rotates opaque refresh tokens."""

from __future__ import annotations

import hashlib
import secrets
from datetime import timedelta
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.exceptions import AuthenticationError
from src.infrastructure.persistence.models.identity import RefreshTokenModel
from src.shared.config.settings import get_settings
from src.shared.utils.clock import utcnow


class RefreshTokenService:
    """Manages refresh tokens using SHA-256 hashed storage."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: UUID) -> str:
        """Generate a raw refresh token, store its hash, return the raw value."""
        raw = secrets.token_urlsafe(48)
        token_hash = self._hash(raw)
        settings = get_settings()
        now = utcnow()
        model = RefreshTokenModel(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=now + timedelta(seconds=settings.refresh_token_ttl_seconds),
        )
        self._session.add(model)
        return raw

    async def consume(self, raw_token: str) -> UUID:
        """Validate, return user_id, and revoke the consumed token (rotation)."""
        token_hash = self._hash(raw_token)
        result = await self._session.execute(
            select(RefreshTokenModel).where(
                RefreshTokenModel.token_hash == token_hash,
                RefreshTokenModel.is_revoked.is_(False),
                RefreshTokenModel.expires_at > utcnow(),
            )
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise AuthenticationError("Invalid or expired refresh token.")
        model.is_revoked = True
        return model.user_id

    async def revoke(self, raw_token: str) -> None:
        """Revoke a specific refresh token."""
        token_hash = self._hash(raw_token)
        result = await self._session.execute(
            select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash)
        )
        model = result.scalar_one_or_none()
        if model:
            model.is_revoked = True

    async def revoke_all(self, user_id: UUID) -> None:
        """Revoke every refresh token belonging to a user (e.g. after password reset)."""
        await self._session.execute(
            update(RefreshTokenModel)
            .where(RefreshTokenModel.user_id == user_id)
            .values(is_revoked=True)
        )

    @staticmethod
    def _hash(raw: str) -> str:
        return hashlib.sha256(raw.encode()).hexdigest()
