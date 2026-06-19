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
