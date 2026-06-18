"""Correlation-id middleware — ensures every request/response carries ``X-Request-ID``."""

from __future__ import annotations

from uuid import uuid4

from starlette.types import ASGIApp, Message, Receive, Scope, Send

_HEADER = b"x-request-id"


class CorrelationIdMiddleware:
    """Generate or propagate an ``X-Request-ID`` correlation header (per §1.4)."""

    def __init__(self, app: ASGIApp) -> None:
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        headers = dict(scope.get("headers") or [])
        request_id = headers.get(_HEADER, str(uuid4()).encode())

        async def send_with_header(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_headers = message.setdefault("headers", [])
                response_headers.append((_HEADER, request_id))
            await send(message)

        await self._app(scope, receive, send_with_header)
