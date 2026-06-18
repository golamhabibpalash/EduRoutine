"""Generic repository port (collection-like abstraction over persistence)."""

from __future__ import annotations

from typing import Protocol, TypeVar
from uuid import UUID

from src.domain.common.entity import Entity

EntityT = TypeVar("EntityT", bound=Entity)


class Repository(Protocol[EntityT]):
    """Minimal collection-oriented repository contract.

    Concrete bounded-context repositories extend this with domain-specific lookups.
    Implementations live in the infrastructure layer.
    """

    async def get(self, entity_id: UUID) -> EntityT | None:
        """Return the entity with ``entity_id`` or ``None`` if absent."""
        ...

    async def add(self, entity: EntityT) -> None:
        """Stage a new entity for persistence."""
        ...

    async def delete(self, entity: EntityT) -> None:
        """Stage an entity for removal."""
        ...
