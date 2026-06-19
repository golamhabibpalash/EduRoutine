"""Tests for the health endpoint (bare response)."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"]
    assert body["version"]
    # Correlation id is echoed back on the response.
    assert response.headers.get("x-request-id")


def test_health_is_public(client: TestClient) -> None:
    assert client.get("/api/v1/health").status_code == 200
