"""Password reset token service — single-use, SHA-256 hashed, time-limited tokens."""

from __future__ import annotations

import hashlib
import secrets
from datetime import timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.exceptions import ValidationError
from src.infrastructure.persistence.models.identity import PasswordResetTokenModel
from src.shared.utils.clock import utcnow

RESET_TOKEN_TTL_SECONDS = 3600  # 1 hour


class PasswordResetService:
    """Issues and consumes single-use password-reset tokens."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: UUID) -> str:
        """Generate a raw reset token, store its hash, and return the raw value."""
        raw = secrets.token_urlsafe(48)
        model = PasswordResetTokenModel(
            user_id=user_id,
            token_hash=self._hash(raw),
            expires_at=utcnow() + timedelta(seconds=RESET_TOKEN_TTL_SECONDS),
        )
        self._session.add(model)
        return raw

    async def consume(self, raw_token: str) -> UUID:
        """Validate a reset token, mark it used, and return the owning user id."""
        result = await self._session.execute(
            select(PasswordResetTokenModel).where(
                PasswordResetTokenModel.token_hash == self._hash(raw_token),
                PasswordResetTokenModel.used_at.is_(None),
                PasswordResetTokenModel.expires_at > utcnow(),
            )
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise ValidationError("Invalid or expired password reset token.")
        model.used_at = utcnow()
        return model.user_id

    @staticmethod
    def _hash(raw: str) -> str:
        return hashlib.sha256(raw.encode()).hexdigest()
