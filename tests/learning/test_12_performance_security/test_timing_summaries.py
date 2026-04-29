"""Learning tests for summarizing multiple response-time observations."""

from __future__ import annotations

import pytest

from src.utils.performance import percentile, summarize_timings


@pytest.mark.performance
def test_timing_summary_calculates_key_metrics() -> None:
    timings_ms = [120, 180, 200, 300, 500]

    summary = summarize_timings(timings_ms)

    assert summary == {
        "count": 5,
        "min_ms": 120,
        "average_ms": 260,
        "p95_ms": 500,
        "max_ms": 500,
    }


@pytest.mark.performance
def test_percentile_uses_nearest_rank_for_learning_examples() -> None:
    assert percentile([10, 20, 30, 40, 50], 50) == 30
    assert percentile([10, 20, 30, 40, 50], 95) == 50


@pytest.mark.performance
def test_empty_timing_samples_are_invalid() -> None:
    with pytest.raises(ValueError, match="at least one timing"):
        summarize_timings([])

    with pytest.raises(ValueError, match="at least one timing"):
        percentile([], 95)
