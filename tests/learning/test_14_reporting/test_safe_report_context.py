"""Learning tests for safe report context generation."""

from __future__ import annotations

import pytest
import responses

from src.api_client import APIClient
from src.utils.reporting import (
    build_response_context,
    extract_request_id,
    format_context_for_log,
    truncate_text,
)


@pytest.mark.reporting
@responses.activate
def test_response_context_redacts_sensitive_headers() -> None:
    client = APIClient("https://service.test")
    client.set_bearer_token("secret-token")
    client.session.headers["X-API-Key"] = "api-key-123"
    responses.get(
        "https://service.test/profile",
        json={"error": "forbidden", "request_id": "req-123"},
        status=403,
    )

    response = client.get("/profile")
    context = build_response_context(response)

    assert context["status_code"] == 403
    assert context["request_id"] == "req-123"
    assert context["request_headers"]["Authorization"] == "[REDACTED]"
    assert context["request_headers"]["X-API-Key"] == "[REDACTED]"
    assert "secret-token" not in str(context)
    assert "api-key-123" not in str(context)


@pytest.mark.reporting
@responses.activate
def test_response_context_redacts_sensitive_query_values() -> None:
    client = APIClient("https://service.test")
    responses.get(
        "https://service.test/search?access_token=url-secret&query=orders",
        json={"items": []},
        status=200,
    )

    response = client.get("/search", params={"access_token": "url-secret", "query": "orders"})
    context = build_response_context(response)

    assert context["url"] == (
        "https://service.test/search?access_token=%5BREDACTED%5D&query=orders"
    )
    assert "url-secret" not in str(context)


@pytest.mark.reporting
@responses.activate
def test_response_context_can_use_correlation_header() -> None:
    client = APIClient("https://service.test")
    responses.get(
        "https://service.test/orders/42",
        json={"id": 42},
        status=200,
        headers={"X-Correlation-ID": "corr-42"},
    )

    response = client.get("/orders/42")

    assert extract_request_id(response) == "corr-42"


@pytest.mark.reporting
def test_body_preview_is_bounded_for_reports() -> None:
    assert truncate_text("abcdef", max_chars=3) == "abc..."

    with pytest.raises(ValueError, match="max_chars"):
        truncate_text("abcdef", max_chars=-1)


@pytest.mark.reporting
@responses.activate
def test_log_summary_contains_request_outcome_without_body_noise() -> None:
    client = APIClient("https://service.test")
    responses.get(
        "https://service.test/search",
        json={"items": []},
        status=200,
        headers={"X-Request-ID": "req-search"},
    )

    response = client.get("/search")
    context = build_response_context(response)
    log_line = format_context_for_log(context)

    assert log_line == "GET https://service.test/search -> status=200 request_id=req-search"
