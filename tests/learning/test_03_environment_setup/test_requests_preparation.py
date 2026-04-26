"""Requests examples that do not depend on external network calls."""

from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse

import requests


def test_get_request_prepares_query_parameters(
    jsonplaceholder_base_url: str,
) -> None:
    """`params=` should build the query string safely."""
    request = requests.Request(
        method="GET",
        url=f"{jsonplaceholder_base_url}/posts",
        params={"userId": 1},
    )

    prepared = request.prepare()
    parsed_url = urlparse(prepared.url)

    assert prepared.method == "GET"
    assert parsed_url.scheme == "https"
    assert parsed_url.netloc == "jsonplaceholder.typicode.com"
    assert parsed_url.path == "/posts"
    assert parse_qs(parsed_url.query) == {"userId": ["1"]}


def test_post_request_prepares_json_body(
    jsonplaceholder_base_url: str,
) -> None:
    """`json=` should serialize a Python dict and set the JSON header."""
    payload = {
        "title": "Module 03 setup",
        "body": "Prepared locally without sending a network request.",
        "userId": 1,
    }
    request = requests.Request(
        method="POST",
        url=f"{jsonplaceholder_base_url}/posts",
        json=payload,
    )

    prepared = request.prepare()
    body = prepared.body.decode("utf-8") if isinstance(prepared.body, bytes) else prepared.body

    assert prepared.method == "POST"
    assert prepared.headers["Content-Type"] == "application/json"
    assert json.loads(body) == payload


def test_timeout_fixture_documents_future_live_request_policy(
    default_timeout_seconds: int,
) -> None:
    """Live requests introduced later should reuse an explicit timeout."""
    assert isinstance(default_timeout_seconds, int)
    assert default_timeout_seconds == 10
