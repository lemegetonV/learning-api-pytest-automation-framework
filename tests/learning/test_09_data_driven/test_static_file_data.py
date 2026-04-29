"""Data-driven tests using static JSON and CSV files."""

from __future__ import annotations

import pytest

from src.api_client import APIClient
from src.utils import load_csv_data, load_json_data


POST_PAYLOAD_CASES = load_json_data("test-data/module_09/post_payloads.json")
POST_FILTER_ROWS = load_csv_data("test-data/module_09/post_filters.csv")


def _case_ids(cases: list[dict[str, object]]) -> list[str]:
    return [str(case["case_id"]) for case in cases]


@pytest.mark.parametrize("case", POST_PAYLOAD_CASES, ids=_case_ids(POST_PAYLOAD_CASES))
def test_create_post_with_json_file_payloads(
    api_client: APIClient,
    case: dict[str, object],
) -> None:
    """Each JSON object drives one POST request scenario."""
    payload = case["payload"]
    expected_status = case["expected_status"]

    response = api_client.post("/posts", json=payload)
    body = response.json()

    assert response.status_code == expected_status
    assert body["id"] == 101
    for key, expected_value in payload.items():
        assert body[key] == expected_value


@pytest.mark.parametrize("row", POST_FILTER_ROWS, ids=_case_ids(POST_FILTER_ROWS))
def test_filter_posts_with_csv_rows(api_client: APIClient, row: dict[str, str]) -> None:
    """CSV rows are useful for table-shaped query combinations."""
    user_id = int(row["user_id"])
    expected_count = int(row["expected_count"])

    response = api_client.get("/posts", params={"userId": user_id})
    posts = response.json()

    assert response.status_code == 200
    assert len(posts) == expected_count
    assert {post["userId"] for post in posts} == {user_id}
