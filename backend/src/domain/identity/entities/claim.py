"""User claim entity."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.domain.common.entity import Entity


@dataclass(eq=False)
class Claim(Entity):
    """A typed key/value assertion attached to a user (claim-based authorization).

    Mirrors ``identity.user_claims``. Unique per ``(user_id, claim_type, claim_value)``.
    """

    user_id: UUID
    claim_type: str
    claim_value: str
