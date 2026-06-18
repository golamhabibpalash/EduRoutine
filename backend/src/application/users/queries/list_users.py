"""ListUsers query + handler (Phase 1 skeleton — not yet implemented)."""

from __future__ import annotations

from dataclasses import dataclass

from src.application.common.cqrs import Query
from src.application.common.dto.pagination import Page, PageParams
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.users.dto import UserDTO


@dataclass(frozen=True)
class ListUsersQuery(Query):
    """List users with pagination."""

    page: PageParams
    is_active: bool | None = None


class ListUsersHandler:
    """Handles :class:`ListUsersQuery`."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def handle(self, query: ListUsersQuery) -> Page[UserDTO]:
        """Return a page of users. Implemented in a later phase."""
        raise NotImplementedError("ListUsersHandler is a Phase 1 skeleton stub.")
