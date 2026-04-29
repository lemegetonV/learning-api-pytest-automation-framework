"""Fixtures local to the Module 06 pytest feature examples."""

from __future__ import annotations

import pytest


@pytest.fixture
def known_user() -> dict[str, object]:
    """Known JSONPlaceholder user shape used by class and fixture examples."""
    return {
        "id": 1,
        "name": "Leanne Graham",
        "username": "Bret",
        "email": "Sincere@april.biz",
    }
