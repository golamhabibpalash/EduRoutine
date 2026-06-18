"""GetUser query + handler (Phase 1 skeleton — not yet implemented)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.application.common.cqrs import Query
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.users.dto import UserDTO


@dataclass(frozen=True)
class GetUserQuery(Query):
    """Fetch a single user by id."""

    user_id: UUID


class GetUserHandler:
    """Handles :class:`GetUserQuery`."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def handle(self, query: GetUserQuery) -> UserDTO:
        """Return the user. Implemented in a later phase."""
        raise NotImplementedError("GetUserHandler is a Phase 1 skeleton stub.")
