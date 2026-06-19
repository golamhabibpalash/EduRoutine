"""Unit tests for the bare paginated-response helper."""

from __future__ import annotations

from src.presentation.api.common.response_models import PaginatedResponse, paginate


def test_paginate_shape_is_bare() -> None:
    resp = paginate([1, 2, 3], page=2, page_size=3, total_items=7)
    assert isinstance(resp, PaginatedResponse)
    dumped = resp.model_dump()
    assert dumped["data"] == [1, 2, 3]
    assert "status" not in dumped  # bare — no success envelope
    assert "meta" not in dumped
    assert dumped["pagination"]["total_pages"] == 3
    assert dumped["pagination"]["has_next"] is True
    assert dumped["pagination"]["has_previous"] is True


def test_paginate_first_page() -> None:
    resp = paginate([1], page=1, page_size=20, total_items=1)
    assert resp.pagination.has_previous is False
    assert resp.pagination.has_next is False
    assert resp.pagination.total_pages == 1
