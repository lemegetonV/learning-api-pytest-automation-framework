"""Shared pytest fixtures for the learning framework."""

from __future__ import annotations

import pytest


@pytest.fixture
def jsonplaceholder_base_url() -> str:
    """Base URL used by the learning tests from Module 04 onward."""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture
def default_timeout_seconds() -> int:
    """Default request timeout used once live API calls begin."""
    return 10
