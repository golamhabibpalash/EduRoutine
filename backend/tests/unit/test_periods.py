"""DB-free coverage for the Periods module."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_periods_require_auth(client: TestClient) -> None:
    assert client.get("/api/v1/periods").status_code == 401
    assert client.post("/api/v1/periods", json={}).status_code == 401


def test_openapi_exposes_period_routes(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/periods" in paths
    assert "/api/v1/periods/{period_id}" in paths
