"""Learning tests for reporting plugin availability and commands."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[3]
REQUIREMENTS_PATH = PROJECT_ROOT / "requirements.txt"
REPORTS_DIR = PROJECT_ROOT / "reports"
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "api-tests.yml"


@pytest.mark.reporting
def test_pytest_html_plugin_is_installed() -> None:
    assert importlib.util.find_spec("pytest_html") is not None


@pytest.mark.reporting
def test_allure_pytest_plugin_is_installed() -> None:
    assert importlib.util.find_spec("allure_pytest") is not None


@pytest.mark.reporting
def test_reporting_dependencies_are_active() -> None:
    requirements_text = REQUIREMENTS_PATH.read_text(encoding="utf-8")
    active_requirement_lines = [
        line.strip()
        for line in requirements_text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    assert any(line.startswith("pytest-html==") for line in active_requirement_lines)
    assert any(line.startswith("allure-pytest==") for line in active_requirement_lines)


@pytest.mark.reporting
def test_reports_directory_exists_for_generated_artifacts() -> None:
    assert REPORTS_DIR.exists()
    assert REPORTS_DIR.is_dir()


@pytest.mark.reporting
def test_ci_workflow_generates_and_uploads_report_artifacts() -> None:
    workflow_text = WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "--html=reports/pytest-report.html" in workflow_text
    assert "--alluredir=reports/allure-results" in workflow_text
    assert "--junitxml=reports/junit.xml" in workflow_text
    assert "actions/upload-artifact@v4" in workflow_text
    assert "path: reports/" in workflow_text
