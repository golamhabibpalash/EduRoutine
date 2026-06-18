"""Standard success/error envelopes (per contracts/00-api-standards.md §1.5, §7)."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.shared.utils.clock import utcnow

PAYLOAD_VERSION = "1.0"


class Meta(BaseModel):
    """Envelope metadata block."""

    request_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=utcnow)
    version: str = PAYLOAD_VERSION


class SuccessResponse[DataT](BaseModel):
    """Standard success envelope: ``{ status, data, meta }``."""

    status: str = "success"
    data: DataT
    meta: Meta = Field(default_factory=Meta)


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


def build_meta(request_id: UUID | None = None) -> Meta:
    """Build a :class:`Meta` block, reusing a correlation id when provided."""
    return Meta(request_id=request_id or uuid4())
