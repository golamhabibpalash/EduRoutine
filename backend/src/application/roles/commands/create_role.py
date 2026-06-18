"""CreateRole command + handler (Phase 1 skeleton — not yet implemented)."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from src.application.common.cqrs import Command
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.roles.dto import RoleDTO


@dataclass(frozen=True)
class CreateRoleCommand(Command):
    """Intent to create a new role."""

    name: str
    description: str | None = None
    permission_ids: tuple[UUID, ...] = field(default_factory=tuple)


class CreateRoleHandler:
    """Handles :class:`CreateRoleCommand`."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def handle(self, command: CreateRoleCommand) -> RoleDTO:
        """Create a role. Implemented in a later phase."""
        raise NotImplementedError("CreateRoleHandler is a Phase 1 skeleton stub.")
