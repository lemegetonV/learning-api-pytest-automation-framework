"""Regression tests for body redaction before report attachment."""

from __future__ import annotations

import pytest
import responses

from src.api_client import APIClient
from src.utils.reporting import build_response_context, redact_body_text


@pytest.mark.reporting
def test_json_body_redaction_hides_token_fields() -> None:
    body_text = (
        '{"accessToken": "access-secret", "refreshToken": "refresh-secret", '
        '"profile": {"username": "emilys"}}'
    )

    redacted = redact_body_text(body_text)

    assert "access-secret" not in redacted
    assert "refresh-secret" not in redacted
    assert '"accessToken": "[REDACTED]"' in redacted
    assert '"refreshToken": "[REDACTED]"' in redacted
    assert '"username": "emilys"' in redacted


@pytest.mark.reporting
@responses.activate
def test_response_context_body_preview_redacts_auth_tokens() -> None:
    client = APIClient("https://service.test")
    responses.post(
        "https://service.test/auth/login",
        json={
            "username": "emilys",
            "accessToken": "access-secret",
            "refreshToken": "refresh-secret",
        },
        status=200,
    )

    response = client.post("/auth/login", json={"username": "emilys"})
    context = build_response_context(response)

    assert "access-secret" not in context["body_preview"]
    assert "refresh-secret" not in context["body_preview"]
