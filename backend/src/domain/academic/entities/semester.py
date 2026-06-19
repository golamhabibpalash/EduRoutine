"""Semester aggregate root."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Semester(AggregateRoot):
    """A semester within a session. Mirrors ``academic.semesters``."""

    session_id: UUID
    name: str
    number: int
    start_date: date
    end_date: date
    created_at: datetime | None = None
    updated_at: datetime | None = None
