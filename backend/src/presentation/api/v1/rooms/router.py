"""Rooms API router (bare responses)."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.application.common.dto.pagination import PageParams
from src.presentation.api.common.response_models import PaginatedResponse, paginate
from src.presentation.api.dependencies.auth import Principal, require_permission
from src.presentation.api.dependencies.services import RoomServiceDep
from src.presentation.api.v1.rooms.schemas import CreateRoomRequest, RoomData, UpdateRoomRequest

router = APIRouter(tags=["Rooms"])

PageQ = Annotated[int, Query(ge=1)]
SizeQ = Annotated[int, Query(ge=1, le=100)]


@router.get("/rooms", response_model=PaginatedResponse[RoomData], operation_id="listRooms")
async def list_rooms(
    service: RoomServiceDep,
    _p: Annotated[Principal, Depends(require_permission("room:read:*"))],
    page: PageQ = 1,
    page_size: SizeQ = 20,
    type: Annotated[str | None, Query()] = None,
    is_active: Annotated[bool | None, Query()] = None,
) -> PaginatedResponse[RoomData]:
    r = await service.list_rooms(PageParams(page, page_size), type=type, is_active=is_active)
    return paginate(
        [RoomData.from_dto(x) for x in r.items],
        page=r.page,
        page_size=r.page_size,
        total_items=r.total_items,
    )


@router.post("/rooms", response_model=RoomData, status_code=201, operation_id="createRoom")
async def create_room(
    body: CreateRoomRequest,
    service: RoomServiceDep,
    _p: Annotated[Principal, Depends(require_permission("room:create:*"))],
) -> RoomData:
    dto = await service.create(
        code=body.code,
        name=body.name,
        type=body.type.value,
        capacity=body.capacity,
        building=body.building,
        floor=body.floor,
        has_projector=body.has_projector,
        has_computers=body.has_computers,
        has_ac=body.has_ac,
        is_active=body.is_active,
    )
    return RoomData.from_dto(dto)


@router.get("/rooms/{room_id}", response_model=RoomData, operation_id="getRoom")
async def get_room(
    room_id: UUID,
    service: RoomServiceDep,
    _p: Annotated[Principal, Depends(require_permission("room:read:*"))],
) -> RoomData:
    return RoomData.from_dto(await service.get(room_id))


@router.put("/rooms/{room_id}", response_model=RoomData, operation_id="updateRoom")
async def update_room(
    room_id: UUID,
    body: UpdateRoomRequest,
    service: RoomServiceDep,
    _p: Annotated[Principal, Depends(require_permission("room:update:*"))],
) -> RoomData:
    dto = await service.update(
        room_id,
        name=body.name,
        type=body.type.value,
        capacity=body.capacity,
        building=body.building,
        floor=body.floor,
        has_projector=body.has_projector,
        has_computers=body.has_computers,
        has_ac=body.has_ac,
        is_active=body.is_active,
    )
    return RoomData.from_dto(dto)


@router.delete("/rooms/{room_id}", status_code=204, operation_id="deleteRoom")
async def delete_room(
    room_id: UUID,
    service: RoomServiceDep,
    _p: Annotated[Principal, Depends(require_permission("room:delete:*"))],
) -> None:
    await service.delete(room_id)
