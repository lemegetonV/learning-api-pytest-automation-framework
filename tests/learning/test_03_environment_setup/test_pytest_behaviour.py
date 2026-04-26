"""Small pytest examples used by the Module 03 docs."""

from __future__ import annotations

import pytest


@pytest.mark.smoke
def test_plain_assertions_can_check_values() -> None:
    """Pytest uses Python's built-in assert statement."""
    status_code = 200
    response_time_seconds = 0.25

    assert status_code == 200
    assert response_time_seconds < 1


def test_dictionary_contains_expected_keys() -> None:
    """Dictionary assertions mirror the checks used in API response tests."""
    payload = {
        "id": 1,
        "title": "Learning pytest",
        "userId": 10,
    }
    required_fields = {"id", "title", "userId"}

    assert required_fields.issubset(payload.keys()), (
        f"Expected required API fields to be present. "
        f"Missing: {required_fields.difference(payload.keys())}"
    )


def test_lists_can_be_checked_for_shape_and_content() -> None:
    """List checks prepare us for JSON arrays returned by API endpoints."""
    users = [
        {"id": 1, "name": "Ada"},
        {"id": 2, "name": "Grace"},
    ]

    assert len(users) == 2
    assert all("id" in user for user in users)
    assert users[0]["name"] == "Ada"
