"""Routine aggregate root."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Routine(AggregateRoot):
    """A timetable routine (one per department/session/batch/semester)."""

    name: str
    session_id: UUID
    batch_id: UUID
    semester_id: UUID
    department_id: UUID
    status: str = "draft"
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(eq=False)
class RoutineDetail(AggregateRoot):
    """A single slot inside a routine."""

    routine_id: UUID
    course_id: UUID
    teacher_id: UUID
    room_id: UUID
    section_id: UUID
    day_of_week: str
    start_time: str
    end_time: str
    is_lab: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None
