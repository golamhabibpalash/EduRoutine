"""Email address value object."""

from __future__ import annotations

import re
from dataclasses import dataclass

from src.domain.common.exceptions import BusinessRuleViolationError
from src.domain.common.value_object import ValueObject

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
_MAX_LENGTH = 255


@dataclass(frozen=True)
class EmailAddress(ValueObject):
    """A validated, normalized (lowercased) email address."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if len(normalized) > _MAX_LENGTH or not _EMAIL_RE.match(normalized):
            raise BusinessRuleViolationError(f"Invalid email address: {self.value!r}")
        # frozen dataclass — assign normalized form via object.__setattr__
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
