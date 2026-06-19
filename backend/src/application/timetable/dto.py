"""Timetable read-model DTOs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time
from uuid import UUID


@dataclass(frozen=True)
class PeriodDTO:
    id: UUID
    name: str
    period_number: int
    start_time: time
    end_time: time
    duration_minutes: int
    is_break: bool
    created_at: datetime


@dataclass(frozen=True)
class RoutineDTO:
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


@dataclass(frozen=True)
class RoutineDetailDTO:
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
