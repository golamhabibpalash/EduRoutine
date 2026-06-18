"""AddUserClaim command + handler (Phase 1 skeleton — not yet implemented)."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.application.common.cqrs import Command
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.users.dto import ClaimDTO


@dataclass(frozen=True)
class AddUserClaimCommand(Command):
    """Intent to attach a claim to a user."""

    user_id: UUID
    claim_type: str
    claim_value: str


class AddUserClaimHandler:
    """Handles :class:`AddUserClaimCommand`."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def handle(self, command: AddUserClaimCommand) -> ClaimDTO:
        """Add a claim. Implemented in a later phase."""
        raise NotImplementedError("AddUserClaimHandler is a Phase 1 skeleton stub.")
