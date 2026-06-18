"""Base entity and aggregate-root abstractions."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from src.domain.common.domain_event import DomainEvent


@dataclass(eq=False)
class Entity:
    """Base class for domain entities — identity-based equality on :attr:`id`."""

    id: UUID

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return type(self) is type(other) and self.id == other.id

    def __hash__(self) -> int:
        return hash((type(self), self.id))


@dataclass(eq=False)
class AggregateRoot(Entity):
    """An entity that is the entry point to an aggregate and records domain events."""

    _events: list[DomainEvent] = field(default_factory=list, repr=False, kw_only=True)

    def record_event(self, event: DomainEvent) -> None:
        """Append a domain event to be dispatched after persistence."""
        self._events.append(event)

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear the pending domain events."""
        events = list(self._events)
        self._events.clear()
        return events
