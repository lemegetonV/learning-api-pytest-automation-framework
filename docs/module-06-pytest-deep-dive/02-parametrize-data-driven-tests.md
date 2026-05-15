# Parametrize Data-Driven Tests

## The Problem

Without parametrization, tests get copied:

```python
def test_get_post_1(...): ...
def test_get_post_2(...): ...
def test_get_post_50(...): ...
```

The logic is the same. Only the data changes.

## Basic Parametrize

```python
@pytest.mark.parametrize("post_id", [1, 2, 50, 100])
def test_get_post_by_id(jsonplaceholder_base_url, default_timeout_seconds, post_id):
    response = requests.get(
        f"{jsonplaceholder_base_url}/posts/{post_id}",
        timeout=default_timeout_seconds,
    )
    assert response.status_code == 200
    assert response.json()["id"] == post_id
```

Pytest creates one test case per value.

```text
test_get_post_by_id[1]
test_get_post_by_id[2]
test_get_post_by_id[50]
test_get_post_by_id[100]
```

## Multiple Parameters

Use tuples when values belong together.

```python
@pytest.mark.parametrize(
    "endpoint, expected_count",
    [
        ("/posts", 100),
        ("/comments", 500),
        ("/users", 10),
    ],
)
def test_collection_counts(endpoint, expected_count):
    ...
```

Do not stack parametrization when values are paired. Stacking creates every combination.

## Custom IDs

Use `pytest.param(..., id="readable-name")` to make reports easier to scan.

```python
pytest.param(9999, 404, id="missing-post")
```

Readable IDs matter in CI logs.

## Parameter-Level Marks

You can mark one parameter set:

```python
pytest.param(9999, marks=pytest.mark.xfail(reason="missing user"))
```

This is useful when one case documents a known limitation or bug.

## Stacked Parametrize

Stacking creates a cartesian product.

```python
@pytest.mark.parametrize("method", ["GET", "HEAD"])
@pytest.mark.parametrize("endpoint", ["/posts", "/users"])
def test_endpoint_supports_method(method, endpoint):
    ...
```

This creates four tests:

```text
GET /posts
HEAD /posts
GET /users
HEAD /users
```

## When To Use It

Use parametrize when:

- setup is the same
- request shape is the same
- assertions are the same
- only values differ

Use separate tests when each case has different logic or different meaning.

## Code References

- [`test_parametrize.py`](../../tests/learning/test_06_pytest_features/test_parametrize.py)
- [`test_posts.py`](../../tests/learning/test_04_basic_get/test_posts.py) shows repeated patterns that parametrization can reduce later.

## Key Takeaways

- Parametrize turns one test function into many cases.
- Use tuples for paired values.
- Use custom IDs for readable reports.
- Mark individual parameter sets when needed.
- Do not over-parametrize tests with different logic.
