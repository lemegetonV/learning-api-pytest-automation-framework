"""Reusable API client built on top of requests.Session."""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urljoin

import requests

logger = logging.getLogger(__name__)


class APIClient:
    """Small HTTP client wrapper for API test code."""

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.last_response: requests.Response | None = None
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def get(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send a GET request."""
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send a POST request."""
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send a PUT request."""
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send a PATCH request."""
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send a DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)

    def set_bearer_token(self, token: str) -> None:
        """Apply a bearer token to all future requests in this client session."""
        self.session.auth = None
        self.session.headers["Authorization"] = f"Bearer {token}"

    def set_basic_auth(self, username: str, password: str) -> None:
        """Apply HTTP Basic authentication to all future requests."""
        self.session.headers.pop("Authorization", None)
        self.session.auth = (username, password)

    def clear_auth(self) -> None:
        """Remove authentication state from the client session."""
        self.session.headers.pop("Authorization", None)
        self.session.auth = None

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        """Apply framework defaults and send the HTTP request."""
        url = self._build_url(endpoint)
        kwargs.setdefault("timeout", self.timeout)

        logger.info("%s %s", method, url)
        response = self.session.request(method, url, **kwargs)
        self.last_response = response
        logger.info(
            "Response: %s %s",
            response.status_code,
            response.reason,
        )
        return response

    def _build_url(self, endpoint: str) -> str:
        """Build an absolute URL from a relative endpoint."""
        if endpoint.startswith(("http://", "https://")):
            return endpoint
        return urljoin(f"{self.base_url}/", endpoint.lstrip("/"))

    def close(self) -> None:
        """Close the underlying requests session."""
        self.session.close()

    def __enter__(self) -> "APIClient":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
