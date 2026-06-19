"""Section aggregate root."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Section(AggregateRoot):
    """A subdivision of a batch. Mirrors ``academic.sections``."""

    batch_id: UUID
    name: str
    max_capacity: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
