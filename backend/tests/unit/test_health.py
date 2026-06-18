"""Tests for the Phase 1 health endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_returns_success_envelope(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["data"]["status"] == "ok"
    assert body["data"]["service"]
    assert "request_id" in body["meta"]
    # Correlation id is echoed back on the response.
    assert response.headers.get("x-request-id")


def test_health_is_public(client: TestClient) -> None:
    # No Authorization header supplied; must still succeed.
    assert client.get("/api/v1/health").status_code == 200
