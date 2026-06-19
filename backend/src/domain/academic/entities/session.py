"""Academic session aggregate root."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from src.domain.common.entity import AggregateRoot


@dataclass(eq=False)
class Session(AggregateRoot):
    """An academic session/year. Mirrors ``academic.sessions``."""

    name: str
    start_date: date
    end_date: date
    is_current: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def activate(self) -> None:
        """Mark this session as the current one."""
        self.is_current = True
