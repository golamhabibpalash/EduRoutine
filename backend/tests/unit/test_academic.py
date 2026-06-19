"""Phase 3 (Academic Structure) endpoint coverage that needs no database.

Auth gating and request validation short-circuit before any DB query, so these run DB-free.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "method, path",
    [
        ("get", "/api/v1/departments"),
        ("post", "/api/v1/departments"),
        ("get", "/api/v1/sessions"),
        ("post", "/api/v1/sessions"),
        ("get", "/api/v1/semesters"),
        ("get", "/api/v1/batches"),
        ("get", "/api/v1/sections"),
        ("get", "/api/v1/courses"),
    ],
)
def test_academic_endpoints_require_auth(client: TestClient, method: str, path: str) -> None:
    response = client.request(method, path)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_openapi_exposes_academic_routes(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]
    for expected in (
        "/api/v1/departments",
        "/api/v1/sessions",
        "/api/v1/sessions/{session_id}/activate",
        "/api/v1/semesters",
        "/api/v1/batches",
        "/api/v1/batches/{batch_id}/sections",
        "/api/v1/sections",
        "/api/v1/courses",
        "/api/v1/courses/{course_id}/prerequisites",
    ):
        assert expected in paths, f"missing route: {expected}"
