"""User read-model DTOs returned by query handlers (application layer)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class UserDTO:
    """Read model for a user, mapped to ``UserResponse`` in the presentation layer."""

    id: UUID
    email: str
    email_verified: bool
    display_name: str
    phone: str | None
    is_active: bool
    roles: tuple[str, ...]
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class ClaimDTO:
    """Read model for a user claim."""

    id: UUID
    user_id: UUID
    claim_type: str
    claim_value: str
