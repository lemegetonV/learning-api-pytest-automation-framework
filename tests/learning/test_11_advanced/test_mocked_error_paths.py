"""Advanced error-path examples using mocked APIs."""

from __future__ import annotations

import pytest
import requests
import responses

from src.api_client import APIClient


@responses.activate
def test_client_can_assert_structured_500_response_without_live_api() -> None:
    """Mocking lets tests cover rare server failures deterministically."""
    client = APIClient("https://service.test")
    responses.add(
        responses.GET,
        "https://service.test/unstable",
        json={
            "error": "temporary outage",
            "request_id": "req-module-11",
        },
        status=500,
    )

    response = client.get("/unstable")

    assert response.status_code == 500
    assert response.json()["error"] == "temporary outage"
    assert response.json()["request_id"] == "req-module-11"
    assert client.last_response is response


@responses.activate
def test_timeout_exception_can_be_exercised_without_waiting() -> None:
    """Timeout behavior should be tested without making the suite slow."""
    client = APIClient("https://service.test", timeout=1)

    def raise_timeout(_request: requests.PreparedRequest) -> tuple[int, dict[str, str], str]:
        raise requests.Timeout("mocked timeout")

    responses.add_callback(
        responses.GET,
        "https://service.test/slow",
        callback=raise_timeout,
    )

    with pytest.raises(requests.Timeout, match="mocked timeout"):
        client.get("/slow")
