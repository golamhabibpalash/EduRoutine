"""Resource Management application services."""

from __future__ import annotations

from uuid import UUID, uuid4

from src.application.common.dto.pagination import Page, PageParams
from src.application.common.exceptions import ConflictError
from src.application.common.interfaces.unit_of_work import UnitOfWork
from src.application.resources.dto import RoomDTO
from src.domain.resources.entities.room import Room
from src.domain.resources.exceptions import RoomNotFoundError
from src.shared.utils.clock import utcnow


class RoomService:
    """Use cases for the Rooms module."""

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    @staticmethod
    def _dto(r: Room) -> RoomDTO:
        return RoomDTO(
            id=r.id,
            code=r.code,
            name=r.name,
            type=r.type,
            capacity=r.capacity,
            building=r.building,
            floor=r.floor,
            has_projector=r.has_projector,
            has_computers=r.has_computers,
            has_ac=r.has_ac,
            is_active=r.is_active,
            created_at=r.created_at or utcnow(),
            updated_at=r.updated_at or utcnow(),
        )

    async def get(self, room_id: UUID) -> RoomDTO:
        return self._dto(await self._require(room_id))

    async def list_rooms(
        self, page: PageParams, *, type: str | None = None, is_active: bool | None = None
    ) -> Page[RoomDTO]:
        items = await self._uow.rooms.list_page(
            limit=page.limit, offset=page.offset, type=type, is_active=is_active
        )
        total = await self._uow.rooms.count(type=type, is_active=is_active)
        return Page([self._dto(r) for r in items], page.page, page.page_size, total)

    async def create(
        self,
        *,
        code: str,
        name: str,
        type: str,
        capacity: int,
        building: str,
        floor: int,
        has_projector: bool = False,
        has_computers: bool = False,
        has_ac: bool = True,
        is_active: bool = True,
    ) -> RoomDTO:
        if await self._uow.rooms.get_by_code(code) is not None:
            raise ConflictError(f"A room with code '{code}' already exists.")
        room = Room(
            id=uuid4(),
            code=code,
            name=name,
            type=type,
            capacity=capacity,
            building=building,
            floor=floor,
            has_projector=has_projector,
            has_computers=has_computers,
            has_ac=has_ac,
            is_active=is_active,
        )
        await self._uow.rooms.add(room)
        await self._uow.commit()
        return self._dto(room)

    async def update(
        self,
        room_id: UUID,
        *,
        name: str,
        type: str,
        capacity: int,
        building: str,
        floor: int,
        has_projector: bool,
        has_computers: bool,
        has_ac: bool,
        is_active: bool,
    ) -> RoomDTO:
        room = await self._require(room_id)
        room.name = name
        room.type = type
        room.capacity = capacity
        room.building = building
        room.floor = floor
        room.has_projector = has_projector
        room.has_computers = has_computers
        room.has_ac = has_ac
        room.is_active = is_active
        await self._uow.rooms.update(room)
        await self._uow.commit()
        return self._dto(room)

    async def delete(self, room_id: UUID) -> None:
        room = await self._require(room_id)
        await self._uow.rooms.delete(room)
        await self._uow.commit()

    async def _require(self, room_id: UUID) -> Room:
        room = await self._uow.rooms.get(room_id)
        if room is None:
            raise RoomNotFoundError(f"Room '{room_id}' not found.")
        return room
