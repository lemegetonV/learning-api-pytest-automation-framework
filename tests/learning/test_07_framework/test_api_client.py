"""Tests for the reusable APIClient."""

from __future__ import annotations

from unittest.mock import Mock

import pytest
import requests

from src.api_client import APIClient
from src.config import get_settings


def test_client_builds_urls_from_relative_endpoints() -> None:
    """Relative endpoints should be joined to the configured base URL."""
    client = APIClient("https://example.test/api")

    assert client._build_url("/posts/1") == "https://example.test/api/posts/1"
    assert client._build_url("posts/1") == "https://example.test/api/posts/1"


def test_client_accepts_absolute_urls() -> None:
    """Absolute URLs should pass through unchanged."""
    client = APIClient("https://example.test")

    assert (
        client._build_url("https://other.example/posts/1")
        == "https://other.example/posts/1"
    )


def test_client_sets_json_default_headers() -> None:
    """The session should carry JSON-oriented default headers."""
    client = APIClient("https://example.test")

    assert client.session.headers["Accept"] == "application/json"
    assert client.session.headers["Content-Type"] == "application/json"


def test_client_applies_default_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    """Requests without an explicit timeout should use the client default."""
    client = APIClient("https://example.test", timeout=7)
    fake_response = requests.Response()
    fake_response.status_code = 200
    request_mock = Mock(return_value=fake_response)
    monkeypatch.setattr(client.session, "request", request_mock)

    response = client.get("/posts/1")

    assert response is fake_response
    request_mock.assert_called_once_with(
        "GET",
        "https://example.test/posts/1",
        timeout=7,
    )
    assert client.last_response is fake_response


def test_client_allows_per_request_timeout_override(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Per-request kwargs should override client defaults."""
    client = APIClient("https://example.test", timeout=7)
    fake_response = requests.Response()
    fake_response.status_code = 200
    request_mock = Mock(return_value=fake_response)
    monkeypatch.setattr(client.session, "request", request_mock)

    client.get("/posts/1", timeout=2)

    request_mock.assert_called_once_with(
        "GET",
        "https://example.test/posts/1",
        timeout=2,
    )


def test_client_passes_query_params_to_requests(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The wrapper should keep requests keyword arguments available."""
    client = APIClient("https://example.test")
    fake_response = requests.Response()
    fake_response.status_code = 200
    request_mock = Mock(return_value=fake_response)
    monkeypatch.setattr(client.session, "request", request_mock)

    client.get("/posts", params={"userId": 1})

    request_mock.assert_called_once_with(
        "GET",
        "https://example.test/posts",
        params={"userId": 1},
        timeout=10,
    )


def test_context_manager_closes_session(monkeypatch: pytest.MonkeyPatch) -> None:
    """Using APIClient as a context manager should close the session."""
    client = APIClient("https://example.test")
    close_mock = Mock()
    monkeypatch.setattr(client.session, "close", close_mock)

    with client as active_client:
        assert active_client is client

    close_mock.assert_called_once_with()


class TestAPIClientFixture:
    """Live examples that use the framework-level api_client fixture."""

    def test_fixture_uses_configured_settings(self, api_client: APIClient) -> None:
        settings = get_settings()

        assert api_client.base_url == settings.base_url
        assert api_client.timeout == settings.timeout

    def test_get_single_post_with_client(self, api_client: APIClient) -> None:
        response = api_client.get("/posts/1")

        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_get_with_query_params_with_client(self, api_client: APIClient) -> None:
        response = api_client.get("/posts", params={"userId": 1})

        assert response.status_code == 200
        posts = response.json()
        assert len(posts) > 0
        assert all(post["userId"] == 1 for post in posts)

    def test_post_with_client(self, api_client: APIClient) -> None:
        payload = {
            "title": "Created through APIClient",
            "body": "Module 07 framework test.",
            "userId": 1,
        }

        response = api_client.post("/posts", json=payload)

        assert response.status_code == 201
        created = response.json()
        assert created["title"] == payload["title"]
        assert created["id"] == 101

    def test_delete_with_client(self, api_client: APIClient) -> None:
        response = api_client.delete("/posts/1")

        assert response.status_code == 200
        assert response.json() == {}
