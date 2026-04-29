# Module 11 Exercises: Advanced Testing

## Exercise 1: Mock A 401 Response

Create a test in `tests/learning/test_11_advanced/test_mocked_error_paths.py`.

Mock:

```text
GET https://service.test/protected
```

Return:

```json
{
  "error": "missing token",
  "request_id": "req-401"
}
```

Expected assertions:

- status code is `401`
- `error == "missing token"`
- `request_id == "req-401"`

## Exercise 2: Add A Retryable Status

Read `is_retryable_status()` in `test_flaky_api_patterns.py`.

Answer:

1. Why is `503` retryable?
2. Why is `400` not retryable?
3. Would you retry `POST` requests automatically? Explain the risk.

## Exercise 3: Create A Three-Step Flaky Sequence

Mock one endpoint with:

1. `503`
2. `503`
3. `200`

Expected outcome:

- the first two calls are retryable failures
- the third call succeeds
- `len(responses.calls) == 3`

## Exercise 4: Add A Breaking Version Case

In `test_version_compatibility.py`, create a response where:

- `id` is still an integer
- `name` exists
- `email` is renamed to `emailAddress`

Expected outcome:

- the compatibility contract reports missing `email`
- this is a breaking change for the consumer

## Exercise 5: Consumer Contract Or Provider Schema

For each field, decide whether it belongs in a consumer contract, provider schema, or both:

1. `request_id`, because the client logs it
2. `debug_code`, only used by backend support
3. `error`, shown in test failure output
4. `support_url`, ignored by this client

Explain your choices.

## Exercise 6: Mocking Decision

For each scenario, decide whether to use a live test or mocked test:

1. Check JSONPlaceholder `/posts/1` is reachable.
2. Verify client behavior when an endpoint times out.
3. Validate a rare `500` error body.
4. Confirm real login works in a staging environment.
5. Reproduce `503` followed by `200`.

Explain why.
