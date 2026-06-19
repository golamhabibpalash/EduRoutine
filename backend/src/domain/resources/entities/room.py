"""Room aggregate root."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Room(AggregateRoot):
    """A physical room/lab. Standalone record matching the frontend contract."""

    code: str
    name: str
    type: str
    capacity: int
    building: str
    floor: int
    has_projector: bool = False
    has_computers: bool = False
    has_ac: bool = True
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def deactivate(self) -> None:
        """Soft-deactivate the room."""
        self.is_active = False
