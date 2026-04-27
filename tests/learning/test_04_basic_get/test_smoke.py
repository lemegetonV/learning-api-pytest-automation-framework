"""Smoke tests for the first live API calls."""

from __future__ import annotations

import pytest
import requests


@pytest.mark.smoke
def test_jsonplaceholder_is_reachable(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """A basic GET request should reach JSONPlaceholder."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}. URL: {response.url}"
    )


@pytest.mark.smoke
def test_jsonplaceholder_returns_json_content_type(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """JSONPlaceholder should identify JSON responses with Content-Type."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]


@pytest.mark.smoke
def test_single_post_response_has_expected_fields(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """The smallest post smoke check verifies the expected JSON shape."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    post = response.json()
    assert set(post.keys()) == {"userId", "id", "title", "body"}


@pytest.mark.smoke
def test_posts_collection_is_not_empty(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """The posts collection should return at least one item."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0
