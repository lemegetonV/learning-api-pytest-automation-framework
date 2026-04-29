# Basic Auth, Bearer Tokens, And API Keys

APIs support different credential transport patterns. The test framework should make these patterns visible without duplicating low-level code in every test.

## HTTP Basic Auth

Basic auth sends a username and password through the HTTP authentication mechanism. With `requests`, credentials can be stored on a session:

```python
client.set_basic_auth("learner", "secret")
response = client.get("/basic-auth/learner/secret")
```

The helper lives in [`src/api_client/client.py`](../../src/api_client/client.py):

```python
def set_basic_auth(self, username: str, password: str) -> None:
    self.session.headers.pop("Authorization", None)
    self.session.auth = (username, password)
```

The tests live in [`test_basic_auth.py`](../../tests/learning/test_08_auth/test_basic_auth.py).

| Test | Purpose |
| --- | --- |
| `test_basic_auth_accepts_valid_credentials` | Valid username/password returns `200` |
| `test_basic_auth_rejects_invalid_credentials` | Wrong password returns `401` |

## Bearer Tokens

Bearer tokens are usually sent through the `Authorization` header:

```http
Authorization: Bearer module-08-token
```

The framework helper keeps this in one place:

```python
def set_bearer_token(self, token: str) -> None:
    self.session.auth = None
    self.session.headers["Authorization"] = f"Bearer {token}"
```

The tests in [`test_bearer_and_api_keys.py`](../../tests/learning/test_08_auth/test_bearer_and_api_keys.py) verify both success and missing-token failure.

## API Keys

API keys are often sent in one of two places:

| Placement | Example | Risk |
| --- | --- | --- |
| Query string | `/get?api_key=training-key` | Secret appears in URLs, logs, browser history, and proxies |
| Header | `X-API-Key: training-key` | Still sensitive, but not part of the URL |

Module 08 includes both examples because learners should recognize both patterns in real projects.

## Why The Client Owns Auth Helpers

Without a client helper, tests would repeatedly manipulate headers and session auth:

```python
session.headers["Authorization"] = f"Bearer {token}"
session.auth = (username, password)
```

That creates duplication and makes cleanup easy to forget. The auth setter methods act as mode switches:

| Method | Auth state after the call |
| --- | --- |
| `set_basic_auth(...)` | Basic auth is active and any Bearer header is removed |
| `set_bearer_token(...)` | Bearer auth is active and any Basic auth tuple is removed |
| `clear_auth()` | Both Basic auth and Bearer auth are removed |

This matters because `requests` can prepare an `Authorization` header from `session.auth`. If a client kept both Basic auth state and a Bearer header, Basic auth could win at request time. The framework avoids that conflict.

## Code References

- [`src/api_client/client.py`](../../src/api_client/client.py)
- [`test_auth_helpers.py`](../../tests/learning/test_08_auth/test_auth_helpers.py)
- [`test_basic_auth.py`](../../tests/learning/test_08_auth/test_basic_auth.py)
- [`test_bearer_and_api_keys.py`](../../tests/learning/test_08_auth/test_bearer_and_api_keys.py)

## Key Takeaways

- Basic auth is credential-based and easy to demonstrate, but less common in modern public APIs.
- Bearer tokens are header-based and common in OAuth2/JWT-backed APIs.
- API keys in query strings are easy to test but risky for secrets.
- Auth helper methods keep test code focused on behavior and prevent conflicting auth modes.
