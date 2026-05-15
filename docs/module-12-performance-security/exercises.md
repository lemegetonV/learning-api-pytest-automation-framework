# Module 12 Exercises: Performance And Security

## Exercise 1: Add A New Budget Case

Open [`test_response_time_budgets.py`](../../tests/learning/test_12_performance_security/test_response_time_budgets.py).

Add one assertion where:

- elapsed time is exactly equal to the budget
- the expected result is `True`

Hint: a budget is inclusive in this framework.

Expected outcome:

- the test passes
- the assertion documents the boundary behavior

## Exercise 2: Measure A Simple Operation

Create a small test that uses `measure_call()` around a lambda that returns `"ok"`.

Expected assertions:

- `timed.value == "ok"`
- `timed.elapsed_ms >= 0`

Hint: do not assert an exact elapsed time.

## Exercise 3: Interpret Timing Metrics

Given this timing sample:

```python
[100, 110, 120, 130, 900]
```

Answer:

1. What is the average?
2. What is the max?
3. Why does the max matter even if most calls are fast?

Expected outcome:

- you can explain why average alone is incomplete

## Exercise 4: Use A Custom Sensitive Query Parameter

Add a test in [`test_secret_handling.py`](../../tests/learning/test_12_performance_security/test_secret_handling.py) that calls `find_sensitive_query_params()` with a custom sensitive-name set.

Use this URL:

```text
https://service.test/profile?session_id=abc123
```

Pass this custom configuration:

```python
sensitive_names={"session_id"}
```

Expected outcome:

- `find_sensitive_query_params()` returns `["session_id"]`
- the framework code does not need to change just because one project has an extra sensitive parameter name

## Exercise 5: Add A Custom Redaction Case

Write a test where `redact_headers()` receives a custom sensitive header list:

```python
redact_headers(headers, sensitive_names={"x-internal-token"})
```

Expected outcome:

- `X-Internal-Token` is redacted
- unrelated headers remain unchanged

Hint: header comparison is case-insensitive.

## Exercise 6: Header Policy Discussion

For each response type, decide which checks make sense:

1. Public browser HTML page
2. Internal JSON API response
3. File download endpoint
4. Login endpoint

For each one, answer:

- Would you check `Strict-Transport-Security`?
- Would you check `Content-Security-Policy`?
- Would you check that tokens are absent from URLs?

Expected outcome:

- you can explain why security checks depend on endpoint purpose

## Exercise 7: Marker Selection

Run:

```bash
python -m pytest -m performance -v
python -m pytest -m security -v
```

Expected outcome:

- performance-marked tests run separately from security-marked tests
- you can explain how Module 13 could use these markers in CI
