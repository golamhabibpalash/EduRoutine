"""Course aggregate root."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Course(AggregateRoot):
    """A course offering. Mirrors ``academic.courses``."""

    department_id: UUID
    code: str
    title: str
    credits: Decimal
    lecture_hours: int = 0
    lab_hours: int = 0
    is_active: bool = True
    prerequisite_ids: set[UUID] = field(default_factory=set)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def deactivate(self) -> None:
        """Soft-deactivate the course."""
        self.is_active = False
