"""Resource repository ports."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from src.domain.resources.entities.room import Room


class RoomRepository(Protocol):
    """Persistence contract for :class:`Room`."""

    async def get(self, room_id: UUID) -> Room | None: ...
    async def get_by_code(self, code: str) -> Room | None: ...
    async def list_page(
        self, *, limit: int, offset: int, type: str | None = None, is_active: bool | None = None
    ) -> list[Room]: ...
    async def count(self, *, type: str | None = None, is_active: bool | None = None) -> int: ...
    async def add(self, room: Room) -> None: ...
    async def update(self, room: Room) -> None: ...
    async def delete(self, room: Room) -> None: ...


__all__ = ["RoomRepository"]
