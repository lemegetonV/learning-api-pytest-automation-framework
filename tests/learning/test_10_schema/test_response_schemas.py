"""Schema validation tests against JSONPlaceholder responses."""

from __future__ import annotations

import pytest

from src.api_client import APIClient
from src.utils import load_schema, validate_json


@pytest.fixture(scope="module")
def post_schema() -> dict[str, object]:
    """JSONPlaceholder post response schema."""
    return load_schema("schemas/jsonplaceholder/post.schema.json")


@pytest.fixture(scope="module")
def post_collection_schema() -> dict[str, object]:
    """JSONPlaceholder post collection response schema."""
    return load_schema("schemas/jsonplaceholder/post_collection.schema.json")


@pytest.fixture(scope="module")
def comment_schema() -> dict[str, object]:
    """JSONPlaceholder comment response schema."""
    return load_schema("schemas/jsonplaceholder/comment.schema.json")


@pytest.fixture(scope="module")
def user_schema() -> dict[str, object]:
    """JSONPlaceholder user response schema."""
    return load_schema("schemas/jsonplaceholder/user.schema.json")


def test_single_post_matches_schema(api_client: APIClient, post_schema: dict[str, object]) -> None:
    """A single post should match the documented post contract."""
    response = api_client.get("/posts/1")

    assert response.status_code == 200
    validate_json(response.json(), post_schema)


def test_post_collection_items_match_schema(
    api_client: APIClient,
    post_schema: dict[str, object],
) -> None:
    """Collection checks usually validate every item, not only the first one."""
    response = api_client.get("/posts", params={"userId": 1})
    posts = response.json()

    assert response.status_code == 200
    assert len(posts) == 10
    for post in posts:
        validate_json(post, post_schema)


def test_post_collection_matches_array_schema(
    api_client: APIClient,
    post_collection_schema: dict[str, object],
) -> None:
    """A collection schema validates the array and every item shape together."""
    response = api_client.get("/posts", params={"userId": 1})

    assert response.status_code == 200
    validate_json(response.json(), post_collection_schema)


def test_single_comment_matches_schema(
    api_client: APIClient,
    comment_schema: dict[str, object],
) -> None:
    """Comments have a different response contract from posts."""
    response = api_client.get("/comments/1")

    assert response.status_code == 200
    validate_json(response.json(), comment_schema)


def test_single_user_matches_nested_schema(
    api_client: APIClient,
    user_schema: dict[str, object],
) -> None:
    """User responses include nested address, geo, and company objects."""
    response = api_client.get("/users/1")

    assert response.status_code == 200
    validate_json(response.json(), user_schema)
