"""Seed initial admin user on first startup (development mode)."""

from __future__ import annotations

from uuid import uuid4

from src.domain.identity.entities.user import User
from src.domain.identity.value_objects.email import EmailAddress
from src.infrastructure.auth.password_hasher import Argon2PasswordHasher
from src.infrastructure.persistence.database import get_sessionmaker
from src.infrastructure.persistence.repositories.user_repository import SqlAlchemyUserRepository
from src.shared.utils.clock import utcnow

ADMIN_EMAIL = "admin@eduroutine.com"
ADMIN_PASSWORD = "Admin123!"
ADMIN_DISPLAY_NAME = "System Administrator"


async def seed_admin_user() -> None:
    """Create the default admin user if it doesn't exist."""
    session_factory = get_sessionmaker()
    async with session_factory() as session:
        repo = SqlAlchemyUserRepository(session)
        email = EmailAddress(ADMIN_EMAIL)
        exists = await repo.exists_by_email(email)
        if exists:
            return

        hasher = Argon2PasswordHasher()
        now = utcnow()
        user = User(
            id=uuid4(),
            email=email,
            password_hash=hasher.hash(ADMIN_PASSWORD),
            display_name=ADMIN_DISPLAY_NAME,
            created_at=now,
            updated_at=now,
        )
        await repo.add(user)
        await session.commit()
