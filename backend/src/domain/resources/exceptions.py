"""Resource-context domain exceptions."""

from __future__ import annotations

from src.domain.common.exceptions import EntityNotFoundError


class RoomNotFoundError(EntityNotFoundError):
    """Raised when a room cannot be located."""
