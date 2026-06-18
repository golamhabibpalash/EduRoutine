"""Password hasher port. Implementation (Argon2) lives in the infrastructure layer."""

from __future__ import annotations

from typing import Protocol


class PasswordHasher(Protocol):
    """Hashes and verifies user passwords."""

    def hash(self, plain_password: str) -> str:
        """Return a salted hash for ``plain_password``."""
        ...

    def verify(self, plain_password: str, password_hash: str) -> bool:
        """Return whether ``plain_password`` matches ``password_hash``."""
        ...
