"""Environment checks for Module 03.

These tests prove the local Python environment can import the packages that
the rest of the framework will build on.
"""

from __future__ import annotations

import sys
from importlib import metadata

import pytest
import requests


def test_python_version_is_supported() -> None:
    """The project requires Python 3.10 or newer."""
    assert sys.version_info >= (3, 10), (
        f"Expected Python 3.10+, got {sys.version_info.major}."
        f"{sys.version_info.minor}.{sys.version_info.micro}"
    )


def test_pytest_is_installed_from_environment() -> None:
    """Pytest should be importable by the interpreter running the tests."""
    assert metadata.version("pytest") == pytest.__version__


def test_requests_is_installed_from_environment() -> None:
    """Requests should be importable before live API tests begin."""
    assert metadata.version("requests") == requests.__version__


def test_shared_url_fixture_uses_https(jsonplaceholder_base_url: str) -> None:
    """The shared base URL should be ready for later API modules."""
    assert jsonplaceholder_base_url == "https://jsonplaceholder.typicode.com"
    assert jsonplaceholder_base_url.startswith("https://")


def test_timeout_fixture_is_positive(default_timeout_seconds: int) -> None:
    """HTTP timeouts should be explicit and positive."""
    assert default_timeout_seconds > 0
