"""POST request tests for creating JSONPlaceholder resources."""

from __future__ import annotations

import requests


def test_create_post_returns_201_and_echoes_payload(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """POST /posts should return 201 and echo the sent JSON body."""
    payload = {
        "title": "Module 05 created post",
        "body": "Testing POST request bodies.",
        "userId": 1,
    }

    response = requests.post(
        f"{jsonplaceholder_base_url}/posts",
        json=payload,
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 201, (
        f"Expected 201 Created, got {response.status_code}"
    )
    created_post = response.json()
    assert created_post["title"] == payload["title"]
    assert created_post["body"] == payload["body"]
    assert created_post["userId"] == payload["userId"]


def test_created_post_has_server_generated_id(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """JSONPlaceholder returns id 101 for simulated post creation."""
    payload = {
        "title": "Generated id check",
        "body": "The client did not send an id.",
        "userId": 1,
    }

    response = requests.post(
        f"{jsonplaceholder_base_url}/posts",
        json=payload,
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 201
    created_post = response.json()
    assert isinstance(created_post["id"], int)
    assert created_post["id"] == 101


def test_create_post_response_has_json_content_type(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """The POST response should be returned as JSON."""
    payload = {
        "title": "Header check",
        "body": "Testing content type.",
        "userId": 1,
    }

    response = requests.post(
        f"{jsonplaceholder_base_url}/posts",
        json=payload,
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 201
    assert "application/json" in response.headers["Content-Type"]


def test_create_post_with_minimal_payload_documents_lenient_api(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """JSONPlaceholder accepts partial payloads that stricter APIs may reject."""
    payload = {"title": "Only a title"}

    response = requests.post(
        f"{jsonplaceholder_base_url}/posts",
        json=payload,
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 201
    created_post = response.json()
    assert created_post["title"] == payload["title"]
    assert "id" in created_post


def test_create_post_with_empty_payload_documents_lenient_api(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """JSONPlaceholder accepts an empty object; many real APIs would not."""
    response = requests.post(
        f"{jsonplaceholder_base_url}/posts",
        json={},
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 201
    created_post = response.json()
    assert created_post == {"id": 101}
