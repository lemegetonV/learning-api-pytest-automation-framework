"""Helpers for safe report and log context in API tests."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import requests

from src.utils.security import redact_headers, redact_url_query_params


DEFAULT_BODY_PREVIEW_CHARS = 500
REQUEST_ID_HEADER_NAMES = (
    "x-request-id",
    "x-correlation-id",
    "x-trace-id",
)


def truncate_text(text: str, max_chars: int = DEFAULT_BODY_PREVIEW_CHARS) -> str:
    """Return a bounded text preview for reports."""
    if max_chars < 0:
        raise ValueError("max_chars must be zero or greater")
    if len(text) <= max_chars:
        return text
    return f"{text[:max_chars]}..."


def is_truncated(text: str, max_chars: int = DEFAULT_BODY_PREVIEW_CHARS) -> bool:
    """Return whether text is longer than the configured preview size."""
    if max_chars < 0:
        raise ValueError("max_chars must be zero or greater")
    return len(text) > max_chars


def find_header_value(headers: Mapping[str, str], expected_name: str) -> str | None:
    """Find a header value by name, ignoring case."""
    expected = expected_name.lower()
    for name, value in headers.items():
        if name.lower() == expected:
            return value
    return None


def extract_request_id(response: requests.Response) -> str | None:
    """Extract a useful request/correlation id from headers or JSON body."""
    for header_name in REQUEST_ID_HEADER_NAMES:
        header_value = find_header_value(response.headers, header_name)
        if header_value:
            return header_value

    try:
        body = response.json()
    except ValueError:
        return None

    if isinstance(body, dict):
        request_id = body.get("request_id") or body.get("requestId")
        if isinstance(request_id, str) and request_id:
            return request_id
    return None


def build_response_context(
    response: requests.Response,
    max_body_chars: int = DEFAULT_BODY_PREVIEW_CHARS,
) -> dict[str, Any]:
    """Build redacted response context that can be attached to reports."""
    request = response.request
    request_headers = dict(request.headers) if request is not None else {}
    raw_url = request.url if request is not None else response.url
    elapsed_ms = response.elapsed.total_seconds() * 1000 if response.elapsed else None

    return {
        "method": request.method if request is not None else None,
        "url": redact_url_query_params(raw_url),
        "status_code": response.status_code,
        "reason": response.reason,
        "elapsed_ms": elapsed_ms,
        "request_id": extract_request_id(response),
        "request_headers": redact_headers(request_headers),
        "response_headers": redact_headers(dict(response.headers)),
        "body_preview": truncate_text(response.text, max_body_chars),
        "body_truncated": is_truncated(response.text, max_body_chars),
    }


def format_context_for_log(context: Mapping[str, Any]) -> str:
    """Return a compact one-line summary for logs and report descriptions."""
    method = context.get("method") or "UNKNOWN"
    url = context.get("url") or "unknown-url"
    status_code = context.get("status_code")
    request_id = context.get("request_id") or "none"

    return (
        f"{method} {url} -> status={status_code} request_id={request_id}"
    )
