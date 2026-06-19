"""Academic-context domain exceptions."""

from __future__ import annotations

from src.domain.common.exceptions import EntityNotFoundError


class DepartmentNotFoundError(EntityNotFoundError):
    """Raised when a department cannot be located."""


class SessionNotFoundError(EntityNotFoundError):
    """Raised when a session cannot be located."""


class SemesterNotFoundError(EntityNotFoundError):
    """Raised when a semester cannot be located."""


class BatchNotFoundError(EntityNotFoundError):
    """Raised when a batch cannot be located."""


class SectionNotFoundError(EntityNotFoundError):
    """Raised when a section cannot be located."""


class CourseNotFoundError(EntityNotFoundError):
    """Raised when a course cannot be located."""
