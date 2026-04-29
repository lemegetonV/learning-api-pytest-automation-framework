"""Learning tests for API response-time budgets."""

from __future__ import annotations

import pytest
import responses

from src.api_client import APIClient
from src.utils.performance import is_within_budget, measure_call


@pytest.mark.performance
def test_budget_helper_separates_fast_and_slow_observations() -> None:
    assert is_within_budget(elapsed_ms=120, budget_ms=250) is True
    assert is_within_budget(elapsed_ms=900, budget_ms=250) is False


@pytest.mark.performance
def test_negative_response_time_budget_is_invalid() -> None:
    with pytest.raises(ValueError, match="budget_ms"):
        is_within_budget(elapsed_ms=10, budget_ms=-1)


@pytest.mark.performance
@responses.activate
def test_mocked_get_request_stays_inside_learning_budget() -> None:
    client = APIClient("https://service.test")
    responses.get(
        "https://service.test/posts/1",
        json={"id": 1, "title": "fast path"},
        status=200,
    )

    timed_response = measure_call(lambda: client.get("/posts/1"))

    assert timed_response.value.status_code == 200
    assert timed_response.value.json()["id"] == 1
    assert is_within_budget(timed_response.elapsed_ms, budget_ms=250)
