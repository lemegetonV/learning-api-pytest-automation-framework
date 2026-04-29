"""Learning tests for framework logs used during report analysis."""

from __future__ import annotations

import logging

import pytest
import responses

from src.api_client import APIClient


@pytest.mark.reporting
@responses.activate
def test_api_client_logs_request_and_response_summary(caplog: pytest.LogCaptureFixture) -> None:
    client = APIClient("https://service.test")
    responses.get("https://service.test/health", json={"ok": True}, status=200)

    with caplog.at_level(logging.INFO, logger="src.api_client.client"):
        response = client.get("/health")

    assert response.status_code == 200
    assert "GET https://service.test/health" in caplog.text
    assert "Response: 200 OK" in caplog.text
