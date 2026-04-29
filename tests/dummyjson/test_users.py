"""DummyJSON capstone tests for users, search, and nested profile objects."""

from __future__ import annotations

import pytest

from src.api_client import APIClient
from src.utils.schema_validator import load_schema, validate_json


pytestmark = [pytest.mark.capstone, pytest.mark.dummyjson]


def test_user_collection_matches_schema(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.get("/users", params={"limit": 3})
    body = response.json()
    schema = load_schema("schemas/dummyjson/user_collection.schema.json")

    assert response.status_code == 200
    validate_json(body, schema)
    assert body["limit"] == 3
    assert len(body["users"]) == 3


def test_single_user_contains_nested_address_and_company(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.get("/users/1")
    body = response.json()
    schema = load_schema("schemas/dummyjson/user.schema.json")

    assert response.status_code == 200
    validate_json(body, schema)
    assert body["username"] == "emilys"
    assert body["address"]["coordinates"]["lat"] != 0
    assert body["company"]["department"]


def test_user_search_finds_expected_public_demo_user(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.get("/users/search", params={"q": "Emily"})
    body = response.json()

    assert response.status_code == 200
    assert any(user["username"] == "emilys" for user in body["users"])
    assert body["total"] >= len(body["users"])
