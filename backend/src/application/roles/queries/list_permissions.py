"""ListPermissions query + handler (Phase 1 skeleton — not yet implemented)."""

from __future__ import annotations

from dataclasses import dataclass

from src.application.common.cqrs import Query
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.roles.dto import PermissionDTO


@dataclass(frozen=True)
class ListPermissionsQuery(Query):
    """List the permission catalog, optionally filtered by module."""

    module: str | None = None


class ListPermissionsHandler:
    """Handles :class:`ListPermissionsQuery`."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def handle(self, query: ListPermissionsQuery) -> list[PermissionDTO]:
        """Return permissions. Implemented in a later phase."""
        raise NotImplementedError("ListPermissionsHandler is a Phase 1 skeleton stub.")
