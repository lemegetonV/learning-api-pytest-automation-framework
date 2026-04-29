"""Learning tests for basic response security header checks."""

from __future__ import annotations

import pytest

from src.utils.security import has_header, missing_security_headers


REQUIRED_BROWSER_SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
]


@pytest.mark.security
def test_header_lookup_is_case_insensitive() -> None:
    headers = {"content-security-policy": "default-src 'self'"}

    assert has_header(headers, "Content-Security-Policy") is True


@pytest.mark.security
def test_missing_security_headers_identifies_gaps() -> None:
    headers = {
        "Content-Security-Policy": "default-src 'self'",
        "X-Content-Type-Options": "nosniff",
    }

    missing = missing_security_headers(headers, REQUIRED_BROWSER_SECURITY_HEADERS)

    assert missing == ["Strict-Transport-Security"]


@pytest.mark.security
def test_api_json_response_may_not_need_every_browser_header() -> None:
    headers = {"Content-Type": "application/json; charset=utf-8"}

    missing = missing_security_headers(headers, REQUIRED_BROWSER_SECURITY_HEADERS)

    assert missing == REQUIRED_BROWSER_SECURITY_HEADERS
