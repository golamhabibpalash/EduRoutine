"""Phase 2 endpoint behavior that does not require a database.

These exercise request validation and the auth gate, both of which short-circuit before any
DB query runs, so they need no PostgreSQL.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "method, path",
    [
        ("get", "/api/v1/users"),
        ("get", "/api/v1/users/me"),
        ("post", "/api/v1/users"),
        ("get", "/api/v1/roles"),
        ("get", "/api/v1/permissions"),
    ],
)
def test_protected_endpoints_require_auth(client: TestClient, method: str, path: str) -> None:
    response = client.request(method, path)
    assert response.status_code == 401
    body = response.json()
    assert body["status"] == "error"
    assert body["error"]["code"] == "UNAUTHORIZED"


def test_register_rejects_short_password(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "new@eduroutine.com", "password": "short", "display_name": "New User"},
    )
    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"


def test_login_validates_body(client: TestClient) -> None:
    response = client.post("/api/v1/auth/login", json={"email": "a@b.com"})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_openapi_exposes_phase2_routes(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]
    for expected in (
        "/api/v1/auth/register",
        "/api/v1/auth/login",
        "/api/v1/users",
        "/api/v1/users/me",
        "/api/v1/users/{user_id}",
        "/api/v1/users/{user_id}/roles",
        "/api/v1/users/{user_id}/claims",
        "/api/v1/roles",
        "/api/v1/roles/{role_id}/permissions",
        "/api/v1/permissions",
    ):
        assert expected in paths, f"missing route: {expected}"
