"""Authentication application service (Phase 1 skeleton).

Implements the base email/password authentication contract only. OAuth2 / social login is
explicitly out of scope for Phase 1 and will be added in a later phase.
"""

from __future__ import annotations

from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.domain.identity.services import PasswordHasher


class AuthenticationService:
    """Coordinates credential verification and token issuance.

    Token services (JWT issue/verify, refresh-token store) are injected in later phases. Methods
    are stubs in the Phase 1 skeleton.
    """

    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self._uow = uow
        self._hasher = password_hasher

    async def authenticate(self, email: str, password: str) -> None:
        """Verify credentials and issue tokens. Implemented in a later phase."""
        raise NotImplementedError("AuthenticationService.authenticate is a Phase 1 skeleton stub.")
