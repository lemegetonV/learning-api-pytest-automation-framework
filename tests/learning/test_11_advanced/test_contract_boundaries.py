"""Advanced contract-testing boundary examples."""

from __future__ import annotations

import responses

from src.api_client import APIClient
from src.utils import collect_validation_errors, validate_json


ERROR_CONTRACT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Error Response Contract",
    "type": "object",
    "required": ["error", "request_id"],
    "properties": {
        "error": {"type": "string", "minLength": 1},
        "request_id": {"type": "string", "minLength": 1},
    },
    "additionalProperties": True,
}


@responses.activate
def test_consumer_contract_checks_fields_the_client_depends_on() -> None:
    """Consumer contracts focus on the response fields this client actually uses."""
    client = APIClient("https://service.test")
    responses.add(
        responses.GET,
        "https://service.test/orders/missing",
        json={
            "error": "order not found",
            "request_id": "req-404",
            "support_url": "https://service.test/support",
        },
        status=404,
    )

    response = client.get("/orders/missing")

    assert response.status_code == 404
    validate_json(response.json(), ERROR_CONTRACT_SCHEMA)
    assert response.json()["error"] == "order not found"


def test_contract_test_should_ignore_provider_details_not_used_by_consumer() -> None:
    """Strict provider schemas and consumer contracts serve different purposes."""
    provider_response = {
        "error": "order not found",
        "request_id": "req-404",
        "debug_code": "ORDER_LOOKUP_EMPTY",
    }

    validate_json(provider_response, ERROR_CONTRACT_SCHEMA)


def test_consumer_contract_catches_missing_dependency_field() -> None:
    """If the client depends on request_id, the contract must require it."""
    provider_response = {"error": "order not found"}

    errors = collect_validation_errors(provider_response, ERROR_CONTRACT_SCHEMA)

    assert len(errors) == 1
    assert "'request_id' is a required property" in errors[0].message
