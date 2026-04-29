"""Examples for testing flaky API behavior deterministically."""

from __future__ import annotations

import responses

from src.api_client import APIClient


def is_retryable_status(status_code: int) -> bool:
    """Return whether a status is commonly safe to retry later."""
    return status_code in {408, 429, 500, 502, 503, 504}


def test_retryable_status_classifier_documents_transient_failures() -> None:
    """A retry policy starts with a clear definition of retryable responses."""
    assert is_retryable_status(503) is True
    assert is_retryable_status(429) is True
    assert is_retryable_status(400) is False
    assert is_retryable_status(404) is False


@responses.activate
def test_sequenced_mock_reproduces_transient_failure_then_recovery() -> None:
    """Sequenced responses make flaky behavior reproducible in a unit-like test."""
    client = APIClient("https://service.test")
    url = "https://service.test/reports/123"
    responses.add(responses.GET, url, json={"error": "try again"}, status=503)
    responses.add(responses.GET, url, json={"id": 123, "status": "ready"}, status=200)

    first_response = client.get("/reports/123")
    second_response = client.get("/reports/123")

    assert first_response.status_code == 503
    assert is_retryable_status(first_response.status_code) is True
    assert second_response.status_code == 200
    assert second_response.json()["status"] == "ready"
    assert len(responses.calls) == 2
