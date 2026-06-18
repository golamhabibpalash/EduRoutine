"""Unit-of-Work dependency (provides the application port to handlers)."""

from __future__ import annotations

from collections.abc import AsyncIterator

from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.infrastructure.persistence.unit_of_work import SqlAlchemyUnitOfWork


async def get_unit_of_work() -> AsyncIterator[UnitOfWork]:
    """Yield an active :class:`UnitOfWork` for the request lifecycle."""
    async with SqlAlchemyUnitOfWork() as uow:
        yield uow
