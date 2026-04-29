"""Fixtures for the DummyJSON capstone suite."""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest

from src.api_client import APIClient
from src.config import get_settings


@pytest.fixture
def dummyjson_client() -> Iterator[APIClient]:
    """Function-scoped client for live DummyJSON API tests."""
    settings = get_settings()
    client = APIClient(base_url=settings.dummyjson_url, timeout=settings.timeout)

    yield client

    client.close()


@pytest.fixture
def dummyjson_credentials() -> dict[str, str]:
    """Public DummyJSON demo credentials, overridable for CI experiments."""
    return {
        "username": os.getenv("DUMMYJSON_USERNAME", "emilys"),
        "password": os.getenv("DUMMYJSON_PASSWORD", "emilyspass"),
    }


@pytest.fixture
def dummyjson_login_data(
    dummyjson_client: APIClient,
    dummyjson_credentials: dict[str, str],
) -> dict[str, object]:
    """Log in once for tests that need real DummyJSON auth tokens."""
    response = dummyjson_client.post(
        "/auth/login",
        json={**dummyjson_credentials, "expiresInMins": 30},
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def authenticated_dummyjson_client(
    dummyjson_client: APIClient,
    dummyjson_login_data: dict[str, object],
) -> APIClient:
    """DummyJSON client with an access token applied."""
    token = dummyjson_login_data["accessToken"]
    assert isinstance(token, str)
    dummyjson_client.set_bearer_token(token)
    return dummyjson_client
