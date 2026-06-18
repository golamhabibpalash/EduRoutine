"""Database session dependency."""

from __future__ import annotations

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.persistence.database import get_session


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Yield a request-scoped async DB session."""
    async for session in get_session():
        yield session
