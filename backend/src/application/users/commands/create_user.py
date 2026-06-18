"""CreateUser command + handler (Phase 1 skeleton — not yet implemented)."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from src.application.common.cqrs import Command
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.users.dto import UserDTO
from src.domain.identity.services import PasswordHasher


@dataclass(frozen=True)
class CreateUserCommand(Command):
    """Intent to create a new user account."""

    email: str
    password: str
    display_name: str
    phone: str | None = None
    is_active: bool = True
    role_ids: tuple[UUID, ...] = field(default_factory=tuple)


class CreateUserHandler:
    """Handles :class:`CreateUserCommand`."""

    def __init__(self, uow: UnitOfWork, password_hasher: PasswordHasher) -> None:
        self._uow = uow
        self._hasher = password_hasher

    async def handle(self, command: CreateUserCommand) -> UserDTO:
        """Create a user. Implemented in a later phase."""
        raise NotImplementedError("CreateUserHandler is a Phase 1 skeleton stub.")
