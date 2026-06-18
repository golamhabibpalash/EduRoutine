"""Argon2id password hasher — concrete implementation of the domain port."""

from __future__ import annotations

from passlib.context import CryptContext


class Argon2PasswordHasher:
    """Hashes/verifies passwords using Argon2id (per docs security standards)."""

    def __init__(self) -> None:
        self._ctx = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash(self, plain_password: str) -> str:
        """Return an Argon2id hash for ``plain_password``."""
        return str(self._ctx.hash(plain_password))

    def verify(self, plain_password: str, password_hash: str) -> bool:
        """Return whether ``plain_password`` matches ``password_hash``."""
        return bool(self._ctx.verify(plain_password, password_hash))
