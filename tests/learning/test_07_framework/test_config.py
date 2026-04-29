"""Tests for centralized settings."""

from __future__ import annotations

import pytest

from src.config import Settings, get_settings


def clear_settings_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove settings env vars so default-value tests stay deterministic."""
    for name in (
        "BASE_URL",
        "HTTPBIN_URL",
        "DUMMYJSON_URL",
        "FAKESTORE_URL",
        "TEST_TIMEOUT",
        "TEST_ENV",
        "LOG_LEVEL",
    ):
        monkeypatch.delenv(name, raising=False)


def test_settings_defaults_point_to_learning_apis(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Default settings should let the project run without a .env file."""
    clear_settings_environment(monkeypatch)
    settings = Settings()

    assert settings.base_url == "https://jsonplaceholder.typicode.com"
    assert settings.httpbin_url == "https://httpbin.org"
    assert settings.dummyjson_url == "https://dummyjson.com"
    assert settings.fakestore_url == "https://fakestoreapi.com"


def test_settings_timeout_is_integer(monkeypatch: pytest.MonkeyPatch) -> None:
    """Timeout should be converted from environment text into an integer."""
    clear_settings_environment(monkeypatch)
    settings = Settings()

    assert isinstance(settings.timeout, int)
    assert settings.timeout == 10


def test_get_settings_returns_settings_instance(monkeypatch: pytest.MonkeyPatch) -> None:
    """The framework should expose one config entry point."""
    clear_settings_environment(monkeypatch)
    settings = get_settings()

    assert isinstance(settings, Settings)
    assert settings.test_env == "local"
    assert settings.log_level == "INFO"


def test_settings_can_read_environment_overrides(monkeypatch: pytest.MonkeyPatch) -> None:
    """Environment variables should override defaults without code changes."""
    monkeypatch.setenv("BASE_URL", "https://example.test")
    monkeypatch.setenv("TEST_TIMEOUT", "3")
    monkeypatch.setenv("TEST_ENV", "ci")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = Settings()

    assert settings.base_url == "https://example.test"
    assert settings.timeout == 3
    assert settings.test_env == "ci"
    assert settings.log_level == "DEBUG"


def test_invalid_integer_environment_value_is_visible(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bad numeric config should fail clearly instead of being ignored."""
    monkeypatch.setenv("TEST_TIMEOUT", "not-a-number")

    with pytest.raises(ValueError):
        Settings()
