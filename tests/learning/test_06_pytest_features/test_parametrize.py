"""Parametrize examples for Module 06."""

from __future__ import annotations

import pytest
import requests


@pytest.mark.parametrize("post_id", [1, 2, 50, 100])
def test_get_post_by_id_with_single_parameter(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
    post_id: int,
) -> None:
    """One test function can validate several post IDs."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/{post_id}",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert response.json()["id"] == post_id


@pytest.mark.parametrize(
    "endpoint, expected_count",
    [
        ("/posts", 100),
        ("/comments", 500),
        ("/albums", 100),
        ("/todos", 200),
        ("/users", 10),
    ],
)
def test_collection_counts_with_multiple_parameters(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
    endpoint: str,
    expected_count: int,
) -> None:
    """Endpoint and expected count are paired values."""
    response = requests.get(
        f"{jsonplaceholder_base_url}{endpoint}",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert len(response.json()) == expected_count


@pytest.mark.parametrize(
    "post_id, expected_status",
    [
        pytest.param(1, 200, id="existing-post"),
        pytest.param(0, 404, id="zero-id"),
        pytest.param(9999, 404, id="missing-post"),
    ],
)
def test_get_post_status_code_with_readable_ids(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
    post_id: int,
    expected_status: int,
) -> None:
    """Custom parameter IDs make verbose pytest output easier to read."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/{post_id}",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "user_id",
    [
        pytest.param(1, id="first-user"),
        pytest.param(10, id="last-user"),
        pytest.param(
            9999,
            id="missing-user",
            marks=pytest.mark.xfail(reason="JSONPlaceholder has no user 9999"),
        ),
    ],
)
def test_get_user_by_id_with_parameter_level_marker(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
    user_id: int,
) -> None:
    """One parameter set is expected to fail and is marked directly."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/users/{user_id}",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert response.json()["id"] == user_id


@pytest.mark.parametrize("method", ["GET", "HEAD"])
@pytest.mark.parametrize("endpoint", ["/posts", "/users", "/comments"])
def test_stacked_parametrize_checks_method_endpoint_product(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
    method: str,
    endpoint: str,
) -> None:
    """Stacked parametrize creates every method and endpoint combination."""
    response = requests.request(
        method,
        f"{jsonplaceholder_base_url}{endpoint}",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200


@pytest.mark.parametrize("field", ["userId", "id", "title", "body"])
def test_post_has_each_expected_field(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
    field: str,
) -> None:
    """A single assertion pattern can be reused for each expected field."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert field in response.json()
