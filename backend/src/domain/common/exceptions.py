"""Domain-layer exceptions (framework-agnostic)."""

from __future__ import annotations


class DomainError(Exception):
    """Base class for all domain errors."""

    code: str = "DOMAIN_ERROR"


class EntityNotFoundError(DomainError):
    """Raised when an aggregate/entity cannot be found by its identity."""

    code = "RESOURCE_NOT_FOUND"


class BusinessRuleViolationError(DomainError):
    """Raised when a domain invariant or business rule is violated."""

    code = "BUSINESS_RULE_VIOLATION"
