"""Period aggregate root."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Period(AggregateRoot):
    """A daily-grid period definition (1st period, 2nd period, …)."""

    name: str
    period_number: int
    start_time: time
    end_time: time
    duration_minutes: int
    is_break: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None
