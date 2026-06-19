"""Department aggregate root."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Department(AggregateRoot):
    """An academic department. Mirrors ``academic.departments``."""

    name: str
    code: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
