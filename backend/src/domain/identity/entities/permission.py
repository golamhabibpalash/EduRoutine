"""Permission entity."""

from __future__ import annotations

from dataclasses import dataclass

from src.domain.common.entity import Entity


@dataclass(eq=False)
class Permission(Entity):
    """A granular, assignable capability in ``{module}:{action}:{scope}`` form.

    Mirrors ``identity.permissions``.
    """

    code: str
    name: str
    module: str
    description: str | None = None
