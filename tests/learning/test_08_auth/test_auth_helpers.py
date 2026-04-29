"""Fast tests for authentication helpers on APIClient."""

from __future__ import annotations

from src.api_client import APIClient


def test_set_bearer_token_adds_authorization_header() -> None:
    """Bearer auth is usually sent in the Authorization header."""
    client = APIClient("https://example.test")

    client.set_bearer_token("module-08-token")

    assert client.session.headers["Authorization"] == "Bearer module-08-token"


def test_set_basic_auth_stores_session_credentials() -> None:
    """Basic auth credentials belong in the session, not in every test URL."""
    client = APIClient("https://example.test")

    client.set_basic_auth("learner", "secret")

    assert client.session.auth == ("learner", "secret")


def test_clear_auth_removes_basic_and_bearer_state() -> None:
    """Tests must be able to remove auth state to avoid cross-test leakage."""
    client = APIClient("https://example.test")
    client.set_basic_auth("learner", "secret")
    client.set_bearer_token("module-08-token")

    client.clear_auth()

    assert "Authorization" not in client.session.headers
    assert client.session.auth is None
