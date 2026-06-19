"""Room request/response schemas (bare, matching the frontend)."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field

from src.application.resources.dto import RoomDTO


class RoomType(StrEnum):
    classroom = "classroom"
    lab = "lab"
    lecture_hall = "lecture_hall"
    seminar_room = "seminar_room"
    conference_room = "conference_room"


class RoomData(BaseModel):
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

    @classmethod
    def from_dto(cls, r: RoomDTO) -> RoomData:
        return cls(
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
            created_at=r.created_at,
            updated_at=r.updated_at,
        )


class CreateRoomRequest(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=100)
    type: RoomType
    capacity: int = Field(ge=1, le=1000)
    building: str = Field(min_length=1, max_length=100)
    floor: int = Field(ge=-5, le=200)
    has_projector: bool = False
    has_computers: bool = False
    has_ac: bool = True
    is_active: bool = True


class UpdateRoomRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: RoomType
    capacity: int = Field(ge=1, le=1000)
    building: str = Field(min_length=1, max_length=100)
    floor: int = Field(ge=-5, le=200)
    has_projector: bool = False
    has_computers: bool = False
    has_ac: bool = True
    is_active: bool = True
