"""Tests for project test-data loading helpers."""

from __future__ import annotations

from src.utils import load_csv_data, load_json_data, project_path


def test_project_path_resolves_from_repo_root() -> None:
    """Data files should be found regardless of the current test file location."""
    path = project_path("test-data/module_09/post_payloads.json")

    assert path.exists()
    assert path.name == "post_payloads.json"


def test_load_json_data_returns_typed_python_values() -> None:
    """JSON preserves numbers, objects, arrays, and strings."""
    cases = load_json_data("test-data/module_09/post_payloads.json")

    assert isinstance(cases, list)
    assert cases[0]["case_id"] == "complete-post"
    assert isinstance(cases[0]["payload"]["userId"], int)
    assert cases[0]["expected_status"] == 201


def test_load_csv_data_returns_text_rows() -> None:
    """CSV cells are text until the test converts them."""
    rows = load_csv_data("test-data/module_09/post_filters.csv")

    assert rows[0] == {
        "case_id": "first-user-posts",
        "user_id": "1",
        "expected_count": "10",
    }
