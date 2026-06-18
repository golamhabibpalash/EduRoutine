"""Pagination DTOs shared by query handlers (per 00-api-standards.md §8)."""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


@dataclass(frozen=True)
class PageParams:
    """Normalized offset-pagination request parameters."""

    page: int = 1
    page_size: int = DEFAULT_PAGE_SIZE

    def __post_init__(self) -> None:
        page = max(1, self.page)
        size = min(max(1, self.page_size), MAX_PAGE_SIZE)
        object.__setattr__(self, "page", page)
        object.__setattr__(self, "page_size", size)

    @property
    def offset(self) -> int:
        """SQL OFFSET for this page."""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """SQL LIMIT for this page."""
        return self.page_size


@dataclass(frozen=True)
class Page[ItemT]:
    """A page of results plus pagination metadata."""

    items: list[ItemT]
    page: int
    page_size: int
    total_items: int

    @property
    def total_pages(self) -> int:
        if self.page_size == 0:
            return 0
        return (self.total_items + self.page_size - 1) // self.page_size

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1
