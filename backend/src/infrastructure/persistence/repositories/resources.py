"""SQLAlchemy adapters for the resources repository ports."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.resources.entities.room import Room
from src.infrastructure.persistence.models.resources import RoomModel


class SqlAlchemyRoomRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _to_domain(m: RoomModel) -> Room:
        return Room(
            id=m.id,
            code=m.code,
            name=m.name,
            type=m.type,
            capacity=m.capacity,
            building=m.building,
            floor=m.floor,
            has_projector=m.has_projector,
            has_computers=m.has_computers,
            has_ac=m.has_ac,
            is_active=m.is_active,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get(self, room_id: UUID) -> Room | None:
        m = await self._session.get(RoomModel, room_id)
        return self._to_domain(m) if m else None

    async def get_by_code(self, code: str) -> Room | None:
        r = await self._session.execute(select(RoomModel).where(RoomModel.code == code))
        m = r.scalar_one_or_none()
        return self._to_domain(m) if m else None

    async def list_page(
        self, *, limit: int, offset: int, type: str | None = None, is_active: bool | None = None
    ) -> list[Room]:
        stmt = select(RoomModel).order_by(RoomModel.code)
        if type is not None:
            stmt = stmt.where(RoomModel.type == type)
        if is_active is not None:
            stmt = stmt.where(RoomModel.is_active.is_(is_active))
        r = await self._session.execute(stmt.limit(limit).offset(offset))
        return [self._to_domain(m) for m in r.scalars()]

    async def count(self, *, type: str | None = None, is_active: bool | None = None) -> int:
        stmt = select(func.count()).select_from(RoomModel)
        if type is not None:
            stmt = stmt.where(RoomModel.type == type)
        if is_active is not None:
            stmt = stmt.where(RoomModel.is_active.is_(is_active))
        r = await self._session.execute(stmt)
        return int(r.scalar_one())

    async def add(self, room: Room) -> None:
        self._session.add(
            RoomModel(
                id=room.id,
                code=room.code,
                name=room.name,
                type=room.type,
                capacity=room.capacity,
                building=room.building,
                floor=room.floor,
                has_projector=room.has_projector,
                has_computers=room.has_computers,
                has_ac=room.has_ac,
                is_active=room.is_active,
            )
        )

    async def update(self, room: Room) -> None:
        m = await self._session.get(RoomModel, room.id)
        if m is None:
            return
        m.name = room.name
        m.type = room.type
        m.capacity = room.capacity
        m.building = room.building
        m.floor = room.floor
        m.has_projector = room.has_projector
        m.has_computers = room.has_computers
        m.has_ac = room.has_ac
        m.is_active = room.is_active

    async def delete(self, room: Room) -> None:
        m = await self._session.get(RoomModel, room.id)
        if m:
            await self._session.delete(m)
