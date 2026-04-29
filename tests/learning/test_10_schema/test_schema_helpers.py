"""Tests for reusable schema validation helpers."""

from __future__ import annotations

import pytest
from jsonschema.exceptions import ValidationError

from src.utils import collect_validation_errors, load_schema, validate_json


def test_load_schema_returns_schema_object() -> None:
    """Schema files should load as dictionaries."""
    schema = load_schema("schemas/jsonplaceholder/post.schema.json")

    assert schema["title"] == "JSONPlaceholder Post"
    assert schema["type"] == "object"


def test_validate_json_accepts_valid_payload() -> None:
    """A valid object should pass without raising an exception."""
    schema = load_schema("schemas/jsonplaceholder/post.schema.json")
    post = {
        "userId": 1,
        "id": 1,
        "title": "Valid post",
        "body": "A valid post body",
    }

    validate_json(post, schema)


def test_validate_json_raises_for_invalid_payload() -> None:
    """Invalid objects should fail clearly."""
    schema = load_schema("schemas/jsonplaceholder/post.schema.json")
    invalid_post = {
        "userId": "1",
        "id": 1,
        "title": "",
        "body": "A body is present",
    }

    with pytest.raises(ValidationError):
        validate_json(invalid_post, schema)


def test_collect_validation_errors_returns_all_errors() -> None:
    """Collecting errors is useful for readable failure analysis."""
    schema = load_schema("schemas/jsonplaceholder/post.schema.json")
    invalid_post = {
        "userId": "1",
        "id": 0,
        "title": "",
        "body": "A body is present",
        "unexpected": "field",
    }

    errors = collect_validation_errors(invalid_post, schema)
    messages = [error.message for error in errors]

    assert len(errors) == 4
    assert any("'1' is not of type 'integer'" in message for message in messages)
    assert any("0 is less than the minimum of 1" in message for message in messages)
    assert any("'' should be non-empty" in message for message in messages)
    assert any("Additional properties are not allowed" in message for message in messages)
