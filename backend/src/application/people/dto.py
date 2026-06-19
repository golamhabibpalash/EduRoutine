"""People read-model DTOs."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class TeacherDTO:
    id: UUID
    employee_id: str
    name: str
    email: str
    phone: str | None
    department: str
    specialization: tuple[str, ...]
    max_hours_per_week: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class StudentDTO:
    id: UUID
    student_id: str
    name: str
    email: str
    phone: str | None
    batch_id: UUID
    batch_name: str | None
    section_id: UUID
    section_name: str | None
    enrollment_year: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
