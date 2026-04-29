"""HTTP Basic authentication examples using httpbin."""

from __future__ import annotations

from src.api_client import APIClient


def test_basic_auth_accepts_valid_credentials(httpbin_client: APIClient) -> None:
    """A protected endpoint should return 200 for valid credentials."""
    httpbin_client.set_basic_auth("learner", "secret")

    response = httpbin_client.get("/basic-auth/learner/secret")
    body = response.json()

    assert response.status_code == 200
    assert body["authenticated"] is True
    assert body["user"] == "learner"


def test_basic_auth_rejects_invalid_credentials(httpbin_client: APIClient) -> None:
    """Negative auth tests prove the endpoint is actually protected."""
    httpbin_client.set_basic_auth("learner", "wrong-password")

    response = httpbin_client.get("/basic-auth/learner/secret")

    assert response.status_code == 401
    assert response.text == ""
