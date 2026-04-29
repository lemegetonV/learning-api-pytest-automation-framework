"""Simulated CRUD lifecycle tests against JSONPlaceholder."""

from __future__ import annotations

import requests


def test_simulated_crud_lifecycle_documents_each_step(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """Run create, read, update, patch, and delete requests in sequence."""
    create_payload = {
        "title": "Lifecycle create",
        "body": "Created during a simulated lifecycle.",
        "userId": 1,
    }
    create_response = requests.post(
        f"{jsonplaceholder_base_url}/posts",
        json=create_payload,
        timeout=default_timeout_seconds,
    )

    assert create_response.status_code == 201
    assert create_response.json()["id"] == 101

    read_response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert read_response.status_code == 200
    assert read_response.json()["id"] == 1

    put_payload = {
        "title": "Lifecycle PUT",
        "body": "Replaced during lifecycle.",
        "userId": 1,
    }
    put_response = requests.put(
        f"{jsonplaceholder_base_url}/posts/1",
        json=put_payload,
        timeout=default_timeout_seconds,
    )

    assert put_response.status_code == 200
    assert put_response.json()["title"] == put_payload["title"]

    patch_response = requests.patch(
        f"{jsonplaceholder_base_url}/posts/1",
        json={"title": "Lifecycle PATCH"},
        timeout=default_timeout_seconds,
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["title"] == "Lifecycle PATCH"

    delete_response = requests.delete(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert delete_response.status_code == 200
    assert delete_response.json() == {}


def test_create_then_delete_created_id_documents_fake_persistence(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """Created IDs are returned but not persisted by JSONPlaceholder."""
    create_response = requests.post(
        f"{jsonplaceholder_base_url}/posts",
        json={"title": "Not persisted", "body": "Fake create.", "userId": 1},
        timeout=default_timeout_seconds,
    )

    assert create_response.status_code == 201
    created_id = create_response.json()["id"]
    assert created_id == 101

    delete_response = requests.delete(
        f"{jsonplaceholder_base_url}/posts/{created_id}",
        timeout=default_timeout_seconds,
    )

    assert delete_response.status_code == 200

    read_response = requests.get(
        f"{jsonplaceholder_base_url}/posts/{created_id}",
        timeout=default_timeout_seconds,
    )

    assert read_response.status_code == 404
    assert read_response.json() == {}


def test_multiple_patch_responses_are_independent_with_fake_persistence(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """Each PATCH response is based on original data, not prior PATCH calls."""
    first_patch = requests.patch(
        f"{jsonplaceholder_base_url}/posts/1",
        json={"title": "First patch title"},
        timeout=default_timeout_seconds,
    )

    assert first_patch.status_code == 200
    assert first_patch.json()["title"] == "First patch title"

    second_patch = requests.patch(
        f"{jsonplaceholder_base_url}/posts/1",
        json={"body": "Second patch body"},
        timeout=default_timeout_seconds,
    )

    assert second_patch.status_code == 200
    second_body = second_patch.json()
    assert second_body["body"] == "Second patch body"
    assert second_body["title"] != "First patch title"
