"""Shared pytest fixtures for the learning framework."""

from __future__ import annotations

import pytest
import requests

from src.api_client import APIClient
from src.config import get_settings


@pytest.fixture(scope="session")
def jsonplaceholder_base_url() -> str:
    """Base URL used by the learning tests from Module 04 onward."""
    return get_settings().base_url


@pytest.fixture(scope="session")
def default_timeout_seconds() -> int:
    """Default request timeout used once live API calls begin."""
    return get_settings().timeout


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


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    """Framework API client configured from centralized settings."""
    settings = get_settings()
    client = APIClient(base_url=settings.base_url, timeout=settings.timeout)

    yield client

    client.close()


@pytest.fixture
def httpbin_client() -> APIClient:
    """Function-scoped API client for request-behavior and auth examples."""
    settings = get_settings()
    client = APIClient(base_url=settings.httpbin_url, timeout=settings.timeout)

    yield client

    client.close()
