"""Base value-object abstraction (immutable, structural equality)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject:
    """Marker base for immutable, self-validating value objects.

    Subclasses are frozen dataclasses compared by structural equality and should validate
    their invariants in ``__post_init__``.
    """
