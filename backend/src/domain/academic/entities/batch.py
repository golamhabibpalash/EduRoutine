"""Batch aggregate root."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Batch(AggregateRoot):
    """A student cohort within a session/department. Mirrors ``academic.batches``."""

    session_id: UUID
    department_id: UUID
    name: str
    code: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
