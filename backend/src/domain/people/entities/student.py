"""Student aggregate root."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Student(AggregateRoot):
    """An enrolled student. Standalone record matching the frontend contract."""

    student_id: str
    name: str
    email: str
    batch_id: UUID
    section_id: UUID
    enrollment_year: int
    phone: str | None = None
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def deactivate(self) -> None:
        self.is_active = False
