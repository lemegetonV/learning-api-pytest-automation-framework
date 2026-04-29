"""Examples showing what schema validation catches and does not catch."""

from __future__ import annotations

from src.api_client import APIClient
from src.utils import collect_validation_errors, load_schema, validate_json


def test_schema_catches_missing_required_fields() -> None:
    """A schema can enforce that required response fields exist."""
    schema = load_schema("schemas/jsonplaceholder/comment.schema.json")
    comment_without_email = {
        "postId": 1,
        "id": 1,
        "name": "Comment name",
        "body": "Comment body",
    }

    errors = collect_validation_errors(comment_without_email, schema)

    assert len(errors) == 1
    assert "'email' is a required property" in errors[0].message


def test_schema_catches_unexpected_fields() -> None:
    """additionalProperties=false turns unknown response keys into contract failures."""
    schema = load_schema("schemas/jsonplaceholder/post.schema.json")
    post_with_extra_field = {
        "userId": 1,
        "id": 1,
        "title": "A valid title",
        "body": "A valid body",
        "debug": True,
    }

    errors = collect_validation_errors(post_with_extra_field, schema)

    assert len(errors) == 1
    assert "Additional properties are not allowed" in errors[0].message


def test_schema_format_checks_need_framework_support() -> None:
    """The framework enables format checking so invalid emails are caught."""
    schema = load_schema("schemas/jsonplaceholder/comment.schema.json")
    comment_with_bad_email = {
        "postId": 1,
        "id": 1,
        "name": "Comment name",
        "email": "not-an-email",
        "body": "Comment body",
    }

    errors = collect_validation_errors(comment_with_bad_email, schema)

    assert len(errors) == 1
    assert "'not-an-email' is not a 'email'" in errors[0].message


def test_schema_does_not_replace_business_assertions(
    api_client: APIClient,
) -> None:
    """Schema validation proves shape; test assertions still prove scenario behavior."""
    schema = load_schema("schemas/jsonplaceholder/post.schema.json")

    response = api_client.get("/posts/1")
    post = response.json()

    validate_json(post, schema)
    assert post["id"] == 1
    assert post["userId"] == 1
