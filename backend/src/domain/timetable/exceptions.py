"""Timetable-context domain exceptions."""

from __future__ import annotations

from src.domain.common.exceptions import EntityNotFoundError


class PeriodNotFoundError(EntityNotFoundError):
    """Raised when a period cannot be located."""
