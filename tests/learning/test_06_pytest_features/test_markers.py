"""Marker examples for Module 06."""

from __future__ import annotations

import sys

import pytest
import requests


@pytest.mark.skip(reason="Demonstration only: /v2/posts does not exist")
def test_skipped_future_v2_posts_endpoint(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """A skipped test is collected but not executed."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/v2/posts",
        timeout=default_timeout_seconds,
    )
    assert response.status_code == 200


@pytest.mark.skipif(
    sys.version_info < (3, 10),
    reason="Project requires Python 3.10+",
)
def test_skipif_allows_supported_python_versions(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """This runs in the supported project Python range."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200


@pytest.mark.xfail(reason="JSONPlaceholder 404 body is empty, not descriptive")
def test_xfail_documents_missing_error_message(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """An xfail test runs, but the failure is expected."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/9999",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 404
    assert "error" in response.json()


@pytest.mark.xfail(
    strict=True,
    reason="JSONPlaceholder DELETE returns 200 instead of 204",
)
def test_strict_xfail_delete_does_not_return_204(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """Strict xfail would fail the suite if this unexpectedly passed."""
    response = requests.delete(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 204


@pytest.mark.smoke
def test_smoke_marker_for_api_health(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """A smoke test should be quick and high signal."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/1",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert "application/json" in response.headers["Content-Type"]


@pytest.mark.regression
def test_regression_marker_for_collection_contract(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """A regression test can protect a broader contract."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert len(response.json()) == 100


@pytest.mark.smoke
@pytest.mark.regression
def test_multiple_markers_can_apply_to_one_test(
    jsonplaceholder_base_url: str,
    default_timeout_seconds: int,
) -> None:
    """This test is selected by either smoke or regression marker runs."""
    response = requests.get(
        f"{jsonplaceholder_base_url}/users",
        timeout=default_timeout_seconds,
    )

    assert response.status_code == 200
    assert len(response.json()) > 0
