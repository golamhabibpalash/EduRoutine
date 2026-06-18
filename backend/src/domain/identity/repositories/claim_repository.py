"""Claim repository port."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from src.domain.identity.entities.claim import Claim


class ClaimRepository(Protocol):
    """Persistence contract for user :class:`Claim` entries."""

    async def get(self, claim_id: UUID) -> Claim | None:
        """Return the claim by id, or ``None``."""
        ...

    async def list_for_user(self, user_id: UUID) -> list[Claim]:
        """Return all claims belonging to a user."""
        ...

    async def add(self, claim: Claim) -> None:
        """Stage a new claim for persistence."""
        ...

    async def delete(self, claim: Claim) -> None:
        """Stage a claim for removal."""
        ...
