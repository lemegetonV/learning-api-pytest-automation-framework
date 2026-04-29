"""Test class examples for Module 06."""

from __future__ import annotations

import pytest
import requests


class TestPostRetrieval:
    """Related read tests can be grouped in a class."""

    def test_get_single_post(
        self,
        jsonplaceholder_base_url: str,
        default_timeout_seconds: int,
    ) -> None:
        response = requests.get(
            f"{jsonplaceholder_base_url}/posts/1",
            timeout=default_timeout_seconds,
        )

        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_get_all_posts(
        self,
        jsonplaceholder_base_url: str,
        default_timeout_seconds: int,
    ) -> None:
        response = requests.get(
            f"{jsonplaceholder_base_url}/posts",
            timeout=default_timeout_seconds,
        )

        assert response.status_code == 200
        assert len(response.json()) == 100

    def test_filter_posts_by_user(
        self,
        jsonplaceholder_base_url: str,
        default_timeout_seconds: int,
    ) -> None:
        response = requests.get(
            f"{jsonplaceholder_base_url}/posts",
            params={"userId": 1},
            timeout=default_timeout_seconds,
        )

        assert response.status_code == 200
        assert all(post["userId"] == 1 for post in response.json())


@pytest.mark.regression
class TestPostValidation:
    """A class marker applies to every method in the class."""

    def test_post_has_expected_fields(
        self,
        jsonplaceholder_base_url: str,
        default_timeout_seconds: int,
    ) -> None:
        response = requests.get(
            f"{jsonplaceholder_base_url}/posts/1",
            timeout=default_timeout_seconds,
        )

        assert response.status_code == 200
        assert set(response.json().keys()) == {"userId", "id", "title", "body"}

    def test_post_id_is_integer(
        self,
        jsonplaceholder_base_url: str,
        default_timeout_seconds: int,
    ) -> None:
        response = requests.get(
            f"{jsonplaceholder_base_url}/posts/1",
            timeout=default_timeout_seconds,
        )

        assert response.status_code == 200
        assert isinstance(response.json()["id"], int)

    def test_post_title_is_nonempty_string(
        self,
        jsonplaceholder_base_url: str,
        default_timeout_seconds: int,
    ) -> None:
        response = requests.get(
            f"{jsonplaceholder_base_url}/posts/1",
            timeout=default_timeout_seconds,
        )

        assert response.status_code == 200
        title = response.json()["title"]
        assert isinstance(title, str)
        assert len(title) > 0


class TestUserWithAutouseFixture:
    """Autouse setup can be useful for read-only class data."""

    @pytest.fixture(autouse=True)
    def fetch_user(
        self,
        api_session: requests.Session,
        default_timeout_seconds: int,
    ) -> None:
        """Fetch user 1 before each test method in this class."""
        response = api_session.get(
            f"{api_session.base_url}/users/1",
            timeout=default_timeout_seconds,
        )
        assert response.status_code == 200
        self.user = response.json()

    def test_user_has_name(self) -> None:
        assert "name" in self.user
        assert len(self.user["name"]) > 0

    def test_user_has_email(self) -> None:
        assert "email" in self.user
        assert "@" in self.user["email"]

    def test_user_has_address(self) -> None:
        assert "address" in self.user
        assert "city" in self.user["address"]


class TestApiSessionFixture:
    """The global api_session fixture is shared and closed by teardown."""

    def test_session_has_default_headers(
        self,
        api_session: requests.Session,
    ) -> None:
        assert api_session.headers["Accept"] == "application/json"
        assert api_session.headers["Content-Type"] == "application/json"

    def test_session_has_base_url(
        self,
        api_session: requests.Session,
    ) -> None:
        assert api_session.base_url == "https://jsonplaceholder.typicode.com"

    def test_session_can_make_requests(
        self,
        api_session: requests.Session,
        default_timeout_seconds: int,
    ) -> None:
        response = api_session.get(
            f"{api_session.base_url}/posts/1",
            timeout=default_timeout_seconds,
        )

        assert response.status_code == 200
        assert response.json()["id"] == 1


def test_local_known_user_fixture_is_available(known_user: dict[str, object]) -> None:
    """Local conftest fixtures are available to tests in this directory."""
    assert known_user["id"] == 1
    assert known_user["username"] == "Bret"
