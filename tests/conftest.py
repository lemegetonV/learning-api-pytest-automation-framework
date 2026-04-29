"""Shared pytest fixtures for the learning framework."""

from __future__ import annotations

import pytest
import requests


@pytest.fixture(scope="session")
def jsonplaceholder_base_url() -> str:
    """Base URL used by the learning tests from Module 04 onward."""
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def default_timeout_seconds() -> int:
    """Default request timeout used once live API calls begin."""
    return 10


@pytest.fixture(scope="session")
def api_session(jsonplaceholder_base_url: str) -> requests.Session:
    """Shared requests session with default JSON headers."""
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    )
    session.base_url = jsonplaceholder_base_url

    yield session

    session.close()
