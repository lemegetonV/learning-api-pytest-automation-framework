"""API version compatibility and consumer-contract examples."""

from __future__ import annotations

import responses

from src.api_client import APIClient
from src.utils import collect_validation_errors, validate_json


USER_SUMMARY_COMPATIBLE_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Compatible User Summary",
    "type": "object",
    "required": ["id", "name", "email"],
    "properties": {
        "id": {"type": "integer", "minimum": 1},
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
    },
    "additionalProperties": True,
}


def test_additive_v2_response_remains_backward_compatible() -> None:
    """Adding optional fields should not break consumers of stable fields."""
    v1_user = {"id": 1, "name": "Ada Lovelace", "email": "ada@example.test"}
    v2_user = {
        "id": 1,
        "name": "Ada Lovelace",
        "email": "ada@example.test",
        "timezone": "UTC",
        "links": {"self": "/v2/users/1"},
    }

    validate_json(v1_user, USER_SUMMARY_COMPATIBLE_SCHEMA)
    validate_json(v2_user, USER_SUMMARY_COMPATIBLE_SCHEMA)


def test_breaking_v2_response_is_caught_by_contract() -> None:
    """Removing or changing stable fields is a compatibility break."""
    breaking_user = {
        "id": "1",
        "name": "Ada Lovelace",
        "links": {"self": "/v2/users/1"},
    }

    errors = collect_validation_errors(breaking_user, USER_SUMMARY_COMPATIBLE_SCHEMA)
    messages = [error.message for error in errors]

    assert len(errors) == 2
    assert any("'email' is a required property" in message for message in messages)
    assert any("'1' is not of type 'integer'" in message for message in messages)


@responses.activate
def test_mocked_v1_and_v2_endpoints_share_consumer_contract() -> None:
    """A consumer contract can validate multiple API versions consistently."""
    client = APIClient("https://service.test")
    responses.add(
        responses.GET,
        "https://service.test/v1/users/1",
        json={"id": 1, "name": "Ada Lovelace", "email": "ada@example.test"},
        status=200,
    )
    responses.add(
        responses.GET,
        "https://service.test/v2/users/1",
        json={
            "id": 1,
            "name": "Ada Lovelace",
            "email": "ada@example.test",
            "timezone": "UTC",
        },
        status=200,
    )

    for endpoint in ("/v1/users/1", "/v2/users/1"):
        response = client.get(endpoint)

        assert response.status_code == 200
        validate_json(response.json(), USER_SUMMARY_COMPATIBLE_SCHEMA)
