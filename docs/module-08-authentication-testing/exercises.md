# Module 08 Exercises: Authentication Testing

## Exercise 1: Explain The Status Code

Run:

```bash
python -m pytest tests/learning/test_08_auth/test_basic_auth.py -v
```

Expected outcome:

- The valid credential test returns `200`.
- The invalid credential test returns `401`.

In your own words, explain why `401` is the correct failure code here.

## Exercise 2: Add A Missing Basic Auth Test

Add a test that calls:

```text
GET /basic-auth/learner/secret
```

Do not call `set_basic_auth`.

Expected assertions:

- status code is `401`
- the response body is empty

Hint: use the `httpbin_client` fixture.

## Exercise 3: Compare API Key Placement

Read `tests/learning/test_08_auth/test_bearer_and_api_keys.py`.

Answer:

1. Which test puts the API key in the URL?
2. Which test keeps the API key out of the URL?
3. Why is the header approach usually safer?

## Exercise 4: Prove Cookie Isolation

Create a new test in `tests/learning/test_08_auth/test_cookies_and_sessions.py`.

Steps:

1. Assert the session has no `session_id` cookie at the start.
2. Set the cookie with `/cookies/set/session_id/module-08`.
3. Assert the cookie exists after the response.

Expected outcome:

- The first assertion passes because `httpbin_client` is function-scoped.
- The final assertion passes because one client session keeps cookies between calls.

## Exercise 5: Explain OAuth2 In One Paragraph

Read `04-oauth2-and-jwt-nuance.md`.

Write a short paragraph that includes these words correctly:

- bearer token
- JWT
- OAuth2
- scope
- refresh token

## Exercise 6: Clean Up Auth State

Run:

```python
from src.api_client import APIClient

client = APIClient("https://example.test")
client.set_basic_auth("learner", "secret")
client.set_bearer_token("token")
client.clear_auth()
```

Expected outcome:

- `client.session.auth` is `None`.
- `Authorization` is not present in `client.session.headers`.

Explain why cleanup matters in a shared test session.
