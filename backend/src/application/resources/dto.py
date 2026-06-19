"""Resource read-model DTOs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class RoomDTO:
    id: UUID
    code: str
    name: str
    type: str
    capacity: int
    building: str
    floor: int
    has_projector: bool
    has_computers: bool
    has_ac: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
