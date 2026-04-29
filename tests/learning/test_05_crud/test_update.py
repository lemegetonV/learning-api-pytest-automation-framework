"""PUT and PATCH request tests for JSONPlaceholder resources."""

from __future__ import annotations

import requests


def test_put_replaces_post_and_preserves_id(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """PUT /posts/1 should return a full replacement response with id 1."""
    payload = {
        "title": "Module 05 PUT title",
        "body": "Replacing the full post body.",
        "userId": 1,
    }

    response = requests.put(
        f"{jsonplaceholder_base_url}/posts/1",
        json=payload,
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    updated_post = response.json()
    assert updated_post["id"] == 1
    assert updated_post["title"] == payload["title"]
    assert updated_post["body"] == payload["body"]
    assert updated_post["userId"] == payload["userId"]


def test_put_response_has_json_content_type(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """PUT responses should be returned as JSON."""
    payload = {
        "title": "Content type check",
        "body": "Checking PUT headers.",
        "userId": 1,
    }

    response = requests.put(
        f"{jsonplaceholder_base_url}/posts/1",
        json=payload,
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]


def test_put_nonexistent_post_documents_jsonplaceholder_500(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """JSONPlaceholder returns 500 for PUT on a missing post."""
    payload = {
        "title": "Ghost post",
        "body": "This post does not exist.",
        "userId": 1,
    }

    response = requests.put(
        f"{jsonplaceholder_base_url}/posts/9999",
        json=payload,
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 500


def test_patch_updates_only_title_and_preserves_other_fields(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """PATCH /posts/1 should merge a title update into the existing post."""
    payload = {"title": "Module 05 PATCH title"}

    response = requests.patch(
        f"{jsonplaceholder_base_url}/posts/1",
        json=payload,
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    patched_post = response.json()
    assert patched_post["id"] == 1
    assert patched_post["title"] == payload["title"]
    assert "body" in patched_post
    assert "userId" in patched_post


def test_patch_updates_body_and_preserves_id(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """PATCH can update one body field without changing resource identity."""
    payload = {"body": "Only the body changed."}

    response = requests.patch(
        f"{jsonplaceholder_base_url}/posts/1",
        json=payload,
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    patched_post = response.json()
    assert patched_post["id"] == 1
    assert patched_post["body"] == payload["body"]


def test_patch_with_unknown_field_documents_lenient_api(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """JSONPlaceholder accepts unknown fields; stricter APIs may reject them."""
    payload = {"notARealField": "still echoed by the fake API"}

    response = requests.patch(
        f"{jsonplaceholder_base_url}/posts/1",
        json=payload,
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    patched_post = response.json()
    assert patched_post["id"] == 1
    assert patched_post["notARealField"] == payload["notARealField"]
