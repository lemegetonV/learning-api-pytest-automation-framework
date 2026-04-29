"""DummyJSON capstone tests for products, search, categories, and pagination."""

from __future__ import annotations

import pytest

from src.api_client import APIClient
from src.utils.schema_validator import load_schema, validate_json


pytestmark = [pytest.mark.capstone, pytest.mark.dummyjson]


def test_single_product_has_nested_ecommerce_shape(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.get("/products/1")
    body = response.json()
    schema = load_schema("schemas/dummyjson/product.schema.json")

    assert response.status_code == 200
    validate_json(body, schema)
    assert body["id"] == 1
    assert body["title"]
    assert body["dimensions"]["width"] > 0
    assert body["reviews"]


def test_product_pagination_uses_limit_and_skip(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.get("/products", params={"limit": 5, "skip": 10})
    body = response.json()
    schema = load_schema("schemas/dummyjson/product_collection.schema.json")

    assert response.status_code == 200
    validate_json(body, schema)
    assert body["limit"] == 5
    assert body["skip"] == 10
    assert len(body["products"]) == 5
    assert body["total"] > body["skip"]


def test_product_search_returns_paginated_results(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.get(
        "/products/search",
        params={"q": "phone", "limit": 3},
    )
    body = response.json()
    schema = load_schema("schemas/dummyjson/product_collection.schema.json")

    assert response.status_code == 200
    validate_json(body, schema)
    assert body["limit"] == 3
    assert body["total"] >= len(body["products"])
    assert body["products"]


def test_product_categories_drive_category_endpoint(dummyjson_client: APIClient) -> None:
    categories_response = dummyjson_client.get("/products/categories")
    categories = categories_response.json()
    first_category = categories[0]

    category_response = dummyjson_client.get(
        f"/products/category/{first_category['slug']}",
        params={"limit": 5},
    )
    body = category_response.json()

    assert categories_response.status_code == 200
    assert first_category["slug"]
    assert first_category["url"].endswith(first_category["slug"])
    assert category_response.status_code == 200
    assert body["products"]
    assert all(
        product["category"] == first_category["slug"]
        for product in body["products"]
    )
