"""DummyJSON capstone tests for posts, comments, and user relationships."""

from __future__ import annotations

import pytest

from src.api_client import APIClient
from src.utils.schema_validator import load_schema, validate_json


pytestmark = [pytest.mark.capstone, pytest.mark.dummyjson]


def test_posts_collection_matches_schema(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.get("/posts", params={"limit": 3})
    body = response.json()
    schema = load_schema("schemas/dummyjson/post_collection.schema.json")

    assert response.status_code == 200
    validate_json(body, schema)
    assert body["limit"] == 3
    assert len(body["posts"]) == 3


def test_posts_can_be_filtered_by_user(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.get("/posts/user/5", params={"limit": 5})
    body = response.json()

    assert response.status_code == 200
    assert body["posts"]
    assert all(post["userId"] == 5 for post in body["posts"])


def test_comments_for_post_have_nested_user_summary(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.get("/comments/post/1")
    body = response.json()
    schema = load_schema("schemas/dummyjson/comment_collection.schema.json")

    assert response.status_code == 200
    validate_json(body, schema)
    assert body["comments"]
    assert all(comment["postId"] == 1 for comment in body["comments"])
    assert all("username" in comment["user"] for comment in body["comments"])
