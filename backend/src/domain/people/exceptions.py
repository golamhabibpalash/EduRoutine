"""People-context domain exceptions."""

from __future__ import annotations

from src.domain.common.exceptions import EntityNotFoundError


class TeacherNotFoundError(EntityNotFoundError):
    """Raised when a teacher cannot be located."""


class StudentNotFoundError(EntityNotFoundError):
    """Raised when a student cannot be located."""
