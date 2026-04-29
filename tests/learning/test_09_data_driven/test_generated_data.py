"""Generated data examples using Faker."""

from __future__ import annotations

import pytest
from faker import Faker

from src.api_client import APIClient


def build_fake_post_payload(seed: int, user_id: int = 1) -> dict[str, object]:
    """Build a repeatable fake post payload from a seed."""
    fake = Faker()
    fake.seed_instance(seed)
    return {
        "title": fake.sentence(nb_words=6).rstrip("."),
        "body": fake.paragraph(nb_sentences=2),
        "userId": user_id,
    }


def test_seeded_faker_payloads_are_repeatable() -> None:
    """Generated data can still be deterministic when it is seeded."""
    first_payload = build_fake_post_payload(seed=2026, user_id=3)
    second_payload = build_fake_post_payload(seed=2026, user_id=3)

    assert first_payload == second_payload


def test_different_faker_seeds_create_different_payloads() -> None:
    """Different seeds are useful when a suite needs varied but reproducible data."""
    first_payload = build_fake_post_payload(seed=2026)
    second_payload = build_fake_post_payload(seed=2027)

    assert first_payload != second_payload


@pytest.mark.parametrize(
    "seed,user_id",
    [
        pytest.param(9001, 1, id="generated-user-1"),
        pytest.param(9002, 7, id="generated-user-7"),
    ],
)
def test_create_post_with_generated_payload(
    api_client: APIClient,
    seed: int,
    user_id: int,
) -> None:
    """Generated payloads should still satisfy the API request contract."""
    payload = build_fake_post_payload(seed=seed, user_id=user_id)

    response = api_client.post("/posts", json=payload)
    body = response.json()

    assert response.status_code == 201
    assert body["id"] == 101
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == user_id
