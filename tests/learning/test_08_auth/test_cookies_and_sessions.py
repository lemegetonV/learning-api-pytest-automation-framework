"""Cookie and session handling examples."""

from __future__ import annotations

from src.api_client import APIClient


def test_session_stores_cookie_after_set_cookie_response(
    httpbin_client: APIClient,
) -> None:
    """A requests.Session keeps cookies between calls from the same client."""
    set_response = httpbin_client.get("/cookies/set/session_id/module-08")
    cookies_response = httpbin_client.get("/cookies")
    cookies_body = cookies_response.json()

    assert set_response.status_code == 200
    assert httpbin_client.session.cookies.get("session_id") == "module-08"
    assert cookies_body["cookies"]["session_id"] == "module-08"


def test_request_level_cookies_do_not_pollute_session_cookie_jar(
    httpbin_client: APIClient,
) -> None:
    """Per-request cookies are useful for one call without changing session state."""
    response = httpbin_client.get("/cookies", cookies={"mode": "learning"})
    body = response.json()

    assert response.status_code == 200
    assert body["cookies"]["mode"] == "learning"
    assert httpbin_client.session.cookies.get("mode") is None
