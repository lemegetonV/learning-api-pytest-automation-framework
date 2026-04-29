"""DummyJSON capstone tests for authentication and token flows."""

from __future__ import annotations

import pytest

from src.api_client import APIClient
from src.utils.reporting import build_response_context
from src.utils.schema_validator import load_schema, validate_json


pytestmark = [pytest.mark.capstone, pytest.mark.dummyjson, pytest.mark.auth]


def test_login_returns_user_identity_and_tokens(
    dummyjson_login_data: dict[str, object],
) -> None:
    schema = load_schema("schemas/dummyjson/auth_login.schema.json")

    validate_json(dummyjson_login_data, schema)

    assert dummyjson_login_data["username"] == "emilys"
    assert dummyjson_login_data["email"] == "emily.johnson@x.dummyjson.com"
    assert isinstance(dummyjson_login_data["accessToken"], str)
    assert isinstance(dummyjson_login_data["refreshToken"], str)


def test_auth_me_uses_bearer_token(
    authenticated_dummyjson_client: APIClient,
) -> None:
    response = authenticated_dummyjson_client.get("/auth/me")
    body = response.json()

    assert response.status_code == 200
    assert body["username"] == "emilys"
    assert body["email"] == "emily.johnson@x.dummyjson.com"
    assert body["id"] == 1


def test_refresh_token_returns_usable_token_pair(
    dummyjson_client: APIClient,
    dummyjson_login_data: dict[str, object],
) -> None:
    response = dummyjson_client.post(
        "/auth/refresh",
        json={"refreshToken": dummyjson_login_data["refreshToken"], "expiresInMins": 30},
    )
    body = response.json()

    assert response.status_code == 200
    assert isinstance(body["accessToken"], str)
    assert isinstance(body["refreshToken"], str)


def test_invalid_login_returns_clear_400_error(dummyjson_client: APIClient) -> None:
    response = dummyjson_client.post(
        "/auth/login",
        json={"username": "emilys", "password": "wrong-password"},
    )
    body = response.json()

    assert response.status_code == 400
    assert body["message"] == "Invalid credentials"


def test_login_report_context_redacts_token_body(
    dummyjson_client: APIClient,
    dummyjson_credentials: dict[str, str],
) -> None:
    response = dummyjson_client.post(
        "/auth/login",
        json={**dummyjson_credentials, "expiresInMins": 30},
    )
    context = build_response_context(response)

    assert response.status_code == 200
    assert "accessToken" in context["body_preview"]
    assert "refreshToken" in context["body_preview"]
    assert response.json()["accessToken"] not in context["body_preview"]
    assert response.json()["refreshToken"] not in context["body_preview"]
