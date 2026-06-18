"""Identity-context domain exceptions."""

from __future__ import annotations

from src.domain.common.exceptions import BusinessRuleViolationError, EntityNotFoundError


class UserNotFoundError(EntityNotFoundError):
    """Raised when a user cannot be located."""


class RoleNotFoundError(EntityNotFoundError):
    """Raised when a role cannot be located."""


class DuplicateEmailError(BusinessRuleViolationError):
    """Raised when registering an email that is already in use."""

    code = "DUPLICATE_RESOURCE"
