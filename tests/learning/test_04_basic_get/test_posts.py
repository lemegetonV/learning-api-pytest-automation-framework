"""GET request tests for the JSONPlaceholder /posts resource."""

from __future__ import annotations

import requests


def test_get_single_post_returns_expected_post(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """GET /posts/1 should return the post with id 1."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200, (
        f"Expected 200, got {response.status_code}. URL: {response.url}"
    )
    post = response.json()
    assert post["id"] == 1
    assert post["userId"] == 1


def test_get_all_posts_returns_100_posts(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """GET /posts should return JSONPlaceholder's 100 teaching posts."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list), f"Expected list, got {type(posts).__name__}"
    assert len(posts) == 100, f"Expected 100 posts, got {len(posts)}"


def test_filter_posts_by_user_id_returns_only_that_users_posts(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """GET /posts?userId=1 should only return posts owned by user 1."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts",
        params={"userId": 1},
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) > 0, "Expected at least one post for userId 1"
    assert all(post["userId"] == 1 for post in posts), (
        "Filtered response included a post for a different user"
    )


def test_posts_are_ordered_by_id(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """GET /posts should return posts in ascending id order."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    posts = response.json()
    ids = [post["id"] for post in posts]
    assert ids == sorted(ids), "Posts are not ordered by ascending id"


def test_post_has_exact_expected_fields(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """A single post should contain the stable JSONPlaceholder fields."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    post = response.json()
    expected_fields = {"userId", "id", "title", "body"}
    actual_fields = set(post.keys())
    assert actual_fields == expected_fields, (
        f"Field mismatch. Missing: {expected_fields - actual_fields}. "
        f"Extra: {actual_fields - expected_fields}."
    )


def test_post_field_types_are_correct(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """Post fields should use the documented JSON types."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    post = response.json()
    assert isinstance(post["id"], int)
    assert isinstance(post["userId"], int)
    assert isinstance(post["title"], str)
    assert isinstance(post["body"], str)


def test_every_post_has_required_fields(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """Every item in the posts collection should have the required fields."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    posts = response.json()
    required_fields = {"userId", "id", "title", "body"}

    for post in posts:
        assert required_fields.issubset(post.keys()), (
            f"Post {post.get('id')} missing fields: "
            f"{required_fields - set(post.keys())}"
        )


def test_post_title_and_body_are_not_empty(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """A post should include readable title and body content."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    post = response.json()
    assert post["title"], "Expected title to be non-empty"
    assert post["body"], "Expected body to be non-empty"


def test_posts_response_has_json_content_type(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """The /posts response should be identified as JSON."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]


def test_single_post_response_time_is_acceptable(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """A basic GET should respond quickly enough for a learning smoke check."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 5, (
        f"Response took {response.elapsed.total_seconds():.2f}s"
    )


def test_get_nonexistent_post_returns_404(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """GET /posts/9999 should document missing-resource behavior."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/9999",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 404, (
        f"Expected 404 for missing post, got {response.status_code}"
    )


def test_nonexistent_post_returns_empty_json_object(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """JSONPlaceholder returns an empty object for a missing post."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/9999",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 404
    assert response.json() == {}
