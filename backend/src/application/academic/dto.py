"""Academic read-model DTOs returned by services."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class DepartmentDTO:
    id: UUID
    name: str
    code: str
    created_at: datetime


@dataclass(frozen=True)
class SessionDTO:
    id: UUID
    name: str
    start_date: date
    end_date: date
    is_current: bool
    created_at: datetime


@dataclass(frozen=True)
class SemesterDTO:
    id: UUID
    session_id: UUID
    name: str
    number: int
    start_date: date
    end_date: date
    created_at: datetime


@dataclass(frozen=True)
class BatchDTO:
    id: UUID
    session_id: UUID
    department_id: UUID
    name: str
    code: str
    created_at: datetime


@dataclass(frozen=True)
class SectionDTO:
    id: UUID
    batch_id: UUID
    name: str
    max_capacity: int
    created_at: datetime


@dataclass(frozen=True)
class CourseDTO:
    id: UUID
    department_id: UUID
    code: str
    title: str
    credits: Decimal
    lecture_hours: int
    lab_hours: int
    is_active: bool
    created_at: datetime
