"""GET request tests for comments and nested post comments."""

from __future__ import annotations

import requests


def test_get_all_comments_returns_500_comments(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """GET /comments should return JSONPlaceholder's 500 comments."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/comments",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) == 500


def test_get_single_comment_returns_expected_comment(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """GET /comments/1 should return comment id 1 for post id 1."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/comments/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    comment = response.json()
    assert comment["id"] == 1
    assert comment["postId"] == 1


def test_get_comments_for_post_returns_only_that_posts_comments(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """GET /posts/1/comments should only return comments for post 1."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1/comments",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    comments = response.json()
    assert isinstance(comments, list)
    assert len(comments) > 0
    assert all(comment["postId"] == 1 for comment in comments)


def test_filter_comments_by_post_id_returns_only_matching_comments(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """GET /comments?postId=1 should only return comments for post 1."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/comments",
        params={"postId": 1},
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0
    assert all(comment["postId"] == 1 for comment in comments)


def test_nested_comments_route_matches_post_id_filter(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """Nested route and query filter should identify the same comments."""
    nested_response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1/comments",
        timeout=default_timeout_seconds,
    )
    filtered_response = requests.get(
        f"{jsonplaceholder_base_url}/comments",
        params={"postId": 1},
        timeout=default_timeout_seconds,
    )

    assert nested_response.status_code == 200
    assert filtered_response.status_code == 200

    nested_ids = sorted(comment["id"] for comment in nested_response.json())
    filtered_ids = sorted(comment["id"] for comment in filtered_response.json())
    assert nested_ids == filtered_ids


def test_comment_has_exact_expected_fields(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """A comment should contain the stable JSONPlaceholder fields."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/comments/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    comment = response.json()
    expected_fields = {"postId", "id", "name", "email", "body"}
    assert set(comment.keys()) == expected_fields


def test_comment_field_types_are_correct(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """Comment fields should use the documented JSON types."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/comments/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    comment = response.json()
    assert isinstance(comment["postId"], int)
    assert isinstance(comment["id"], int)
    assert isinstance(comment["name"], str)
    assert isinstance(comment["email"], str)
    assert isinstance(comment["body"], str)


def test_comment_email_has_basic_email_shape(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """The comment email should have a simple email-like shape."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/comments/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    email = response.json()["email"]
    assert "@" in email
    assert "." in email.split("@", maxsplit=1)[1]
