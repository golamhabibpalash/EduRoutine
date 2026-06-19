"""JWT access-token service (HS256 for Phase 1 bootstrap)."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

import jwt

from src.shared.config.settings import Settings
from src.shared.utils.clock import utcnow


class JWTService:
    """Encodes and decodes JWT access tokens using HS256."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def issue_access_token(self, *, subject: str, claims: dict[str, Any] | None = None) -> str:
        """Create a signed HS256 access token."""
        now = utcnow()
        payload: dict[str, Any] = {
            "iss": self._settings.jwt_issuer,
            "aud": self._settings.jwt_audience,
            "sub": subject,
            "iat": now,
            "exp": now + timedelta(seconds=self._settings.access_token_ttl_seconds),
        }
        if claims:
            payload.update(claims)
        return jwt.encode(
            payload, self._settings.jwt_secret_key, algorithm=self._settings.jwt_algorithm
        )

    def decode(self, token: str) -> dict[str, Any]:
        """Validate and decode a token's claims."""
        return jwt.decode(
            token,
            self._settings.jwt_secret_key,
            algorithms=[self._settings.jwt_algorithm],
            audience=self._settings.jwt_audience,
            issuer=self._settings.jwt_issuer,
        )
