"""DELETE request tests for JSONPlaceholder resources."""

from __future__ import annotations

import requests


def test_delete_post_returns_200_and_empty_object(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """DELETE /posts/1 should return the fake API's empty JSON object."""
    response = requests.delete(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert response.json() == {}


def test_delete_response_has_json_content_type(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """JSONPlaceholder returns a JSON response for DELETE."""
    response = requests.delete(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]


def test_delete_nonexistent_post_documents_lenient_api(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """JSONPlaceholder returns 200 even when the deleted ID does not exist."""
    response = requests.delete(
        f"{jsonplaceholder_base_url}/posts/9999",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert response.json() == {}


def test_delete_then_get_documents_simulated_persistence(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """DELETE succeeds, but JSONPlaceholder does not actually remove data."""
    delete_response = requests.delete(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert delete_response.status_code == 200

    read_response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert read_response.status_code == 200
    assert read_response.json()["id"] == 1
