"""Routine request/response schemas."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.application.timetable.dto import RoutineDTO, RoutineDetailDTO


class RoutineData(BaseModel):
    id: UUID
    name: str
    session_id: UUID
    batch_id: UUID
    semester_id: UUID
    department_id: UUID
    status: str
    session_name: str | None = None
    batch_name: str | None = None
    semester_name: str | None = None
    department_name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def from_dto(cls, d: RoutineDTO) -> RoutineData:
        return cls(
            id=d.id,
            name=d.name,
            session_id=d.session_id,
            batch_id=d.batch_id,
            semester_id=d.semester_id,
            department_id=d.department_id,
            status=d.status,
            session_name=d.session_name,
            batch_name=d.batch_name,
            semester_name=d.semester_name,
            department_name=d.department_name,
            created_at=d.created_at,
            updated_at=d.updated_at,
        )


class CreateRoutineRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    session_id: UUID
    batch_id: UUID
    semester_id: UUID
    department_id: UUID


class UpdateRoutineRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    session_id: UUID
    batch_id: UUID
    semester_id: UUID
    department_id: UUID


class RoutineDetailData(BaseModel):
    id: UUID
    routine_id: UUID
    course_id: UUID
    teacher_id: UUID
    room_id: UUID
    section_id: UUID
    day_of_week: str
    start_time: str
    end_time: str
    is_lab: bool
    course_code: str | None = None
    course_name: str | None = None
    teacher_name: str | None = None
    room_code: str | None = None
    section_name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @classmethod
    def from_dto(cls, d: RoutineDetailDTO) -> RoutineDetailData:
        return cls(
            id=d.id,
            routine_id=d.routine_id,
            course_id=d.course_id,
            teacher_id=d.teacher_id,
            room_id=d.room_id,
            section_id=d.section_id,
            day_of_week=d.day_of_week,
            start_time=d.start_time,
            end_time=d.end_time,
            is_lab=d.is_lab,
            course_code=d.course_code,
            course_name=d.course_name,
            teacher_name=d.teacher_name,
            room_code=d.room_code,
            section_name=d.section_name,
            created_at=d.created_at,
            updated_at=d.updated_at,
        )


class CreateRoutineDetailRequest(BaseModel):
    routine_id: UUID
    course_id: UUID
    teacher_id: UUID
    room_id: UUID
    section_id: UUID
    day_of_week: str = Field(pattern=r"^(sunday|monday|tuesday|wednesday|thursday)$")
    start_time: str = Field(pattern=r"^\d{2}:\d{2}$")
    end_time: str = Field(pattern=r"^\d{2}:\d{2}$")
    is_lab: bool = False


class UpdateRoutineDetailRequest(BaseModel):
    course_id: UUID
    teacher_id: UUID
    room_id: UUID
    section_id: UUID
    day_of_week: str = Field(pattern=r"^(sunday|monday|tuesday|wednesday|thursday)$")
    start_time: str = Field(pattern=r"^\d{2}:\d{2}$")
    end_time: str = Field(pattern=r"^\d{2}:\d{2}$")
    is_lab: bool
