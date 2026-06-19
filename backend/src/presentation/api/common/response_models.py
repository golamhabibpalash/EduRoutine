"""Response models.

Success responses are returned **bare** (the entity object directly, or a
``{data, pagination}`` object for collections) to match the frontend contract.
Error responses remain enveloped: ``{status: "error", error: {...}}``.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.shared.utils.clock import utcnow


class Pagination(BaseModel):
    """Pagination metadata for collection responses."""

    page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class PaginatedResponse[ItemT](BaseModel):
    """Collection response: ``{ data: [...], pagination: {...} }``."""

    data: list[ItemT]
    pagination: Pagination


def paginate[ItemT](
    items: list[ItemT], *, page: int, page_size: int, total_items: int
) -> PaginatedResponse[ItemT]:
    """Build a :class:`PaginatedResponse` from a page of items."""
    total_pages = (total_items + page_size - 1) // page_size if page_size else 0
    return PaginatedResponse(
        data=items,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        ),
    )


class ErrorBody(BaseModel):
    """The ``error`` block of an error envelope."""

    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)
    request_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=utcnow)


class ErrorResponse(BaseModel):
    """Standard error envelope: ``{ status, error }``."""

    status: str = "error"
    error: ErrorBody
