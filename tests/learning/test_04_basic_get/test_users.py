"""GET request tests for the JSONPlaceholder /users resource."""

from __future__ import annotations

import requests


def test_get_all_users_returns_10_users(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """GET /users should return JSONPlaceholder's 10 users."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/users",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) == 10


def test_get_single_user_returns_expected_user(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """GET /users/1 should return the expected teaching user."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/users/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1
    assert user["username"] == "Bret"


def test_user_has_expected_top_level_fields(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """A user should contain the expected top-level fields."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/users/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    user = response.json()
    expected_fields = {
        "id",
        "name",
        "username",
        "email",
        "address",
        "phone",
        "website",
        "company",
    }
    assert set(user.keys()) == expected_fields


def test_user_top_level_field_types_are_correct(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """Nested fields should be dictionaries and scalar fields should be strings."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/users/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    user = response.json()
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str)
    assert isinstance(user["username"], str)
    assert isinstance(user["email"], str)
    assert isinstance(user["phone"], str)
    assert isinstance(user["website"], str)
    assert isinstance(user["address"], dict)
    assert isinstance(user["company"], dict)


def test_user_address_has_expected_nested_fields(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """User address should include a nested geo object."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/users/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    address = response.json()["address"]
    assert set(address.keys()) == {"street", "suite", "city", "zipcode", "geo"}
    assert isinstance(address["geo"], dict)


def test_user_address_geo_has_latitude_and_longitude(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """The address.geo object should expose lat and lng values."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/users/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    geo = response.json()["address"]["geo"]
    assert set(geo.keys()) == {"lat", "lng"}
    assert isinstance(geo["lat"], str)
    assert isinstance(geo["lng"], str)


def test_user_company_has_expected_fields(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """The company object should expose name, catchPhrase, and bs."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/users/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    company = response.json()["company"]
    assert set(company.keys()) == {"name", "catchPhrase", "bs"}


def test_all_users_have_unique_usernames(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """Usernames should be unique across the users collection."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/users",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    users = response.json()
    usernames = [user["username"] for user in users]
    assert len(usernames) == len(set(usernames))


def test_post_user_id_points_to_existing_user(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """A post's userId should point to an existing user resource."""
    post_response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert post_response.status_code == 200
    post = post_response.json()

    user_response = requests.get(
        f"{jsonplaceholder_base_url}/users/{post['userId']}",
        timeout=default_timeout_seconds,
    )

    assert user_response.status_code == 200
    user = user_response.json()
    assert user["id"] == post["userId"]
