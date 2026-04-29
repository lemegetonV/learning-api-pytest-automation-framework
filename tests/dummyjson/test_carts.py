"""DummyJSON capstone tests for cart totals and nested product objects."""

from __future__ import annotations

import pytest

from src.api_client import APIClient
from src.utils.schema_validator import load_schema, validate_json


pytestmark = [pytest.mark.capstone, pytest.mark.dummyjson]


def test_user_cart_collection_matches_schema(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.get("/carts/user/5")
    body = response.json()
    schema = load_schema("schemas/dummyjson/cart_collection.schema.json")

    assert response.status_code == 200
    validate_json(body, schema)
    assert body["total"] >= 1
    assert all(cart["userId"] == 5 for cart in body["carts"])


def test_cart_product_totals_are_internally_consistent(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.get("/carts/user/5")
    cart = response.json()["carts"][0]

    assert response.status_code == 200
    assert cart["totalProducts"] == len(cart["products"])
    assert cart["totalQuantity"] == sum(product["quantity"] for product in cart["products"])
    assert cart["discountedTotal"] <= cart["total"]

    for product in cart["products"]:
        assert product["total"] == pytest.approx(product["price"] * product["quantity"])
        assert product["discountedTotal"] <= product["total"]
