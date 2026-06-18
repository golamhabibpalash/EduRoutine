"""Shared domain building blocks."""

from src.domain.common.entity import AggregateRoot, Entity
from src.domain.common.exceptions import (
    BusinessRuleViolationError,
    DomainError,
    EntityNotFoundError,
)
from src.domain.common.value_object import ValueObject

__all__ = [
    "AggregateRoot",
    "BusinessRuleViolationError",
    "DomainError",
    "Entity",
    "EntityNotFoundError",
    "ValueObject",
]
