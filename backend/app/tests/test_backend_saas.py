from __future__ import annotations

import asyncio

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.auth_service import AuthService
from app.services.scheduler import start_scheduler, stop_scheduler


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_and_token_flow(client: TestClient) -> None:
    response = client.post(
        "/auth/register",
        json={"email": "admin@example.com", "password": "strongpassword", "full_name": "Admin", "role": "admin"},
    )
    assert response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={"username": "admin@example.com", "password": "strongpassword"},
    )
    assert login_response.status_code == 200
    payload = login_response.json()
    assert payload["access_token"]
    assert payload["refresh_token"]


def test_scheduler_can_start_and_stop() -> None:
    start_scheduler()
    stop_scheduler()
