"""Learning tests that treat the CI workflow as project configuration."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "api-tests.yml"
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
REQUIREMENTS_PATH = PROJECT_ROOT / "requirements.txt"


def test_github_actions_workflow_exists() -> None:
    assert WORKFLOW_PATH.exists()


def test_workflow_runs_on_push_pull_request_and_manual_dispatch() -> None:
    workflow_text = WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "push:" in workflow_text
    assert "pull_request:" in workflow_text
    assert "workflow_dispatch:" in workflow_text


def test_workflow_installs_dependencies_and_runs_quality_gates() -> None:
    workflow_text = WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "python -m pip install -r requirements.txt" in workflow_text
    assert "python -m compileall -q src tests" in workflow_text
    assert "python -m pytest $PYTEST_TARGET" in workflow_text


def test_workflow_supports_selectable_test_scopes() -> None:
    workflow_text = WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "TEST_SCOPE" in workflow_text
    assert "-m smoke" in workflow_text
    assert "-m performance" in workflow_text
    assert "-m security" in workflow_text


def test_workflow_documents_optional_parallel_execution() -> None:
    workflow_text = WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "PARALLEL" in workflow_text
    assert "python -m pytest $PYTEST_TARGET -n auto" in workflow_text


def test_pytest_markers_support_ci_test_selection() -> None:
    pyproject_text = PYPROJECT_PATH.read_text(encoding="utf-8")

    assert '"smoke: quick health check tests"' in pyproject_text
    assert '"performance: response-time checks"' in pyproject_text
    assert '"security: introductory security checks"' in pyproject_text


def test_xdist_dependency_is_active_for_parallel_ci_strategy() -> None:
    requirements_text = REQUIREMENTS_PATH.read_text(encoding="utf-8")
    active_requirement_lines = [
        line.strip()
        for line in requirements_text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    assert any(line.startswith("pytest-xdist==") for line in active_requirement_lines)
