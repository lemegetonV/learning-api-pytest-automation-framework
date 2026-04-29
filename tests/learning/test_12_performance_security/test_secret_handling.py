"""Learning tests for token exposure and log-safe redaction."""

from __future__ import annotations

import pytest
import responses

from src.api_client import APIClient
from src.utils.security import find_sensitive_query_params, redact_headers


@pytest.mark.security
def test_redact_headers_hides_sensitive_values_without_mutating_input() -> None:
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer secret-token",
        "X-API-Key": "api-key-123",
    }

    redacted = redact_headers(headers)

    assert redacted == {
        "Accept": "application/json",
        "Authorization": "[REDACTED]",
        "X-API-Key": "[REDACTED]",
    }
    assert headers["Authorization"] == "Bearer secret-token"


@pytest.mark.security
def test_sensitive_query_parameters_are_detected() -> None:
    url = "https://service.test/search?query=python&access_token=secret&user=42"

    assert find_sensitive_query_params(url) == ["access_token"]


@pytest.mark.security
@responses.activate
def test_header_api_key_keeps_secret_out_of_url() -> None:
    client = APIClient("https://service.test")
    client.session.headers["X-API-Key"] = "api-key-123"
    responses.get("https://service.test/profile", json={"ok": True}, status=200)

    response = client.get("/profile")
    sent_headers = redact_headers(response.request.headers)

    assert response.status_code == 200
    assert find_sensitive_query_params(response.request.url) == []
    assert sent_headers["X-API-Key"] == "[REDACTED]"
