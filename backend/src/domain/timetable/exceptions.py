"""Timetable-context domain exceptions."""

from __future__ import annotations

from src.domain.common.exceptions import EntityNotFoundError


class PeriodNotFoundError(EntityNotFoundError):
    """Raised when a period cannot be located."""


class RoutineNotFoundError(EntityNotFoundError):
    """Raised when a routine cannot be located."""


class RoutineDetailNotFoundError(EntityNotFoundError):
    """Raised when a routine detail cannot be located."""
