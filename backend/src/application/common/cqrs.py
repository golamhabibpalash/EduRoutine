"""CQRS primitives — base Command/Query markers and generic handler protocols."""

from __future__ import annotations

from typing import Protocol, TypeVar


class Command:
    """Marker base for write intents (CQRS command side)."""


class Query:
    """Marker base for read intents (CQRS query side)."""


CommandT = TypeVar("CommandT", bound=Command, contravariant=True)
QueryT = TypeVar("QueryT", bound=Query, contravariant=True)
ResultT = TypeVar("ResultT", covariant=True)


class CommandHandler(Protocol[CommandT, ResultT]):
    """Handles a single command type and returns a result."""

    async def handle(self, command: CommandT) -> ResultT:
        """Execute the command."""
        ...


class QueryHandler(Protocol[QueryT, ResultT]):
    """Handles a single query type and returns a read model/DTO."""

    async def handle(self, query: QueryT) -> ResultT:
        """Execute the query."""
        ...
