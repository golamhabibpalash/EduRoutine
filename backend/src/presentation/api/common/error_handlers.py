"""Exception handlers mapping domain/application/HTTP errors to the error envelope."""

from __future__ import annotations

from typing import Any
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.application.common.exceptions import ApplicationError
from src.domain.common.exceptions import DomainError
from src.presentation.api.common.response_models import ErrorBody, ErrorResponse

# Map well-known error codes to HTTP status (see error-response-catalog.md).
_CODE_TO_STATUS: dict[str, int] = {
    "VALIDATION_ERROR": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "RESOURCE_NOT_FOUND": 404,
    "CONFLICT": 409,
    "DUPLICATE_RESOURCE": 409,
    "UNPROCESSABLE_ENTITY": 422,
    "BUSINESS_RULE_VIOLATION": 422,
    "RATE_LIMIT_EXCEEDED": 429,
    "INTERNAL_ERROR": 500,
}


def _request_id(request: Request) -> UUID:
    raw = request.headers.get("X-Request-ID")
    try:
        return UUID(raw) if raw else uuid4()
    except ValueError:
        return uuid4()


def _envelope(
    code: str,
    message: str,
    request_id: UUID,
    details: dict[str, Any] | None = None,
) -> ErrorResponse:
    return ErrorResponse(
        error=ErrorBody(
            code=code,
            message=message,
            request_id=request_id,
            details=details or {},
        )
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Attach the standard exception handlers to the FastAPI app."""

    @app.exception_handler(DomainError)
    async def _handle_domain(request: Request, exc: DomainError) -> JSONResponse:
        rid = _request_id(request)
        status = _CODE_TO_STATUS.get(exc.code, 422)
        body = _envelope(exc.code, str(exc) or exc.code, rid)
        return JSONResponse(status_code=status, content=body.model_dump(mode="json"))

    @app.exception_handler(ApplicationError)
    async def _handle_application(request: Request, exc: ApplicationError) -> JSONResponse:
        rid = _request_id(request)
        status = _CODE_TO_STATUS.get(exc.code, 400)
        body = _envelope(exc.code, str(exc) or exc.code, rid)
        return JSONResponse(status_code=status, content=body.model_dump(mode="json"))

    @app.exception_handler(RequestValidationError)
    async def _handle_validation(request: Request, exc: RequestValidationError) -> JSONResponse:
        rid = _request_id(request)
        fields = [
            {
                "field": ".".join(str(p) for p in err.get("loc", []) if p != "body"),
                "code": err.get("type", "invalid"),
                "message": err.get("msg", ""),
            }
            for err in exc.errors()
        ]
        body = _envelope("VALIDATION_ERROR", "Request validation failed.", rid, {"fields": fields})
        return JSONResponse(status_code=400, content=body.model_dump(mode="json"))

    @app.exception_handler(StarletteHTTPException)
    async def _handle_http(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        rid = _request_id(request)
        code = {404: "RESOURCE_NOT_FOUND", 401: "UNAUTHORIZED", 403: "FORBIDDEN"}.get(
            exc.status_code, "HTTP_ERROR"
        )
        body = _envelope(code, str(exc.detail), rid)
        return JSONResponse(status_code=exc.status_code, content=body.model_dump(mode="json"))

    @app.exception_handler(Exception)
    async def _handle_unexpected(request: Request, exc: Exception) -> JSONResponse:
        rid = _request_id(request)
        body = _envelope(
            "INTERNAL_ERROR",
            "An unexpected error occurred. Quote the request_id when contacting support.",
            rid,
        )
        return JSONResponse(status_code=500, content=body.model_dump(mode="json"))
