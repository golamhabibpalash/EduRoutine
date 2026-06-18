"""Application-layer exceptions."""

from __future__ import annotations


class ApplicationError(Exception):
    """Base class for application/use-case errors."""

    code: str = "INTERNAL_ERROR"


class ValidationError(ApplicationError):
    """Raised when a request fails semantic (cross-field/business) validation."""

    code = "UNPROCESSABLE_ENTITY"


class AuthenticationError(ApplicationError):
    """Raised when authentication fails."""

    code = "UNAUTHORIZED"


class PermissionDeniedError(ApplicationError):
    """Raised when the caller lacks the required permission."""

    code = "FORBIDDEN"


class ConflictError(ApplicationError):
    """Raised on a uniqueness/state conflict."""

    code = "CONFLICT"


__all__ = [
    "ApplicationError",
    "AuthenticationError",
    "ConflictError",
    "PermissionDeniedError",
    "ValidationError",
]
