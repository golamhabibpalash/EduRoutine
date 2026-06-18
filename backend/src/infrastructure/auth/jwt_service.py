"""JWT access-token service (Phase 1 skeleton).

Issues/validates short-lived access tokens. Phase 1 bootstraps with the HS256 secret from
settings; RS256 + JWKS key rotation (docs/06) is wired in a later phase. Refresh-token rotation
and the Redis store are also deferred.
"""

from __future__ import annotations

from typing import Any

from src.shared.config.settings import Settings


class JWTService:
    """Encodes and decodes JWT access tokens."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def issue_access_token(self, *, subject: str, claims: dict[str, Any]) -> str:
        """Create a signed access token. Implemented in a later phase."""
        raise NotImplementedError("JWTService.issue_access_token is a Phase 1 skeleton stub.")

    def decode(self, token: str) -> dict[str, Any]:
        """Validate and decode a token's claims. Implemented in a later phase."""
        raise NotImplementedError("JWTService.decode is a Phase 1 skeleton stub.")
