"""Base domain-event abstraction."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from src.shared.utils.clock import utcnow


@dataclass(frozen=True, kw_only=True)
class DomainEvent:
    """Something meaningful that happened in the domain.

    Concrete events subclass this and add their own payload fields.
    """

    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=utcnow)
