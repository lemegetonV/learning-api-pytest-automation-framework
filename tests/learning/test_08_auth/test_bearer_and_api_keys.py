"""Bearer token and API key authentication examples."""

from __future__ import annotations

from src.api_client import APIClient


def test_bearer_token_allows_access_to_token_endpoint(
    httpbin_client: APIClient,
) -> None:
    """Bearer tokens are sent through the Authorization header."""
    httpbin_client.set_bearer_token("module-08-token")

    response = httpbin_client.get("/bearer")
    body = response.json()

    assert response.status_code == 200
    assert body["authenticated"] is True
    assert body["token"] == "module-08-token"


def test_missing_bearer_token_is_rejected(httpbin_client: APIClient) -> None:
    """The same protected endpoint should reject missing credentials."""
    response = httpbin_client.get("/bearer")

    assert response.status_code == 401


def test_api_key_in_query_string_is_visible_in_response_url(
    httpbin_client: APIClient,
) -> None:
    """Query-string API keys work, but they are exposed in URLs and logs."""
    response = httpbin_client.get("/get", params={"api_key": "training-key"})
    body = response.json()

    assert response.status_code == 200
    assert body["args"]["api_key"] == "training-key"
    assert "api_key=training-key" in body["url"]


def test_api_key_header_keeps_secret_out_of_query_string(
    httpbin_client: APIClient,
) -> None:
    """Header-based API keys avoid placing secrets in the request URL."""
    response = httpbin_client.get("/headers", headers={"X-API-Key": "training-key"})
    body = response.json()

    assert response.status_code == 200
    assert body["headers"]["X-Api-Key"] == "training-key"
    assert "training-key" not in response.url
