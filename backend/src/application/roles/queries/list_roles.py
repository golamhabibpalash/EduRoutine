"""ListRoles query + handler (Phase 1 skeleton — not yet implemented)."""

from __future__ import annotations

from dataclasses import dataclass

from src.application.common.cqrs import Query
from src.application.common.dto.pagination import Page, PageParams
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.roles.dto import RoleDTO


@dataclass(frozen=True)
class ListRolesQuery(Query):
    """List roles with pagination."""

    page: PageParams


class ListRolesHandler:
    """Handles :class:`ListRolesQuery`."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def handle(self, query: ListRolesQuery) -> Page[RoleDTO]:
        """Return a page of roles. Implemented in a later phase."""
        raise NotImplementedError("ListRolesHandler is a Phase 1 skeleton stub.")
