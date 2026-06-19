"""Teacher aggregate root."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Teacher(AggregateRoot):
    """A teaching staff member. Standalone record matching the frontend contract."""

    employee_id: str
    name: str
    email: str
    department: str
    phone: str | None = None
    specialization: list[str] = field(default_factory=list)
    max_hours_per_week: int = 30
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def deactivate(self) -> None:
        self.is_active = False
