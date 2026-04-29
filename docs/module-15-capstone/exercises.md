# Module 15 Exercises: DummyJSON Capstone

## Exercise 1: Add A Product Select Test

DummyJSON supports selecting fields with the `select` query parameter.

Add a test in `tests/dummyjson/test_products.py` that calls:

```text
GET /products?limit=2&select=title,price
```

Expected outcome:

- status code is `200`
- every product has `title` and `price`
- the test explains whether extra fields are allowed by the API

## Exercise 2: Add A User Search Case

Add a parametrized test for user searches:

```python
("Emily", "emilys")
("Michael", "michaelw")
```

Expected outcome:

- each query returns at least one user
- the expected username appears in the result set

Hint: verify the live user names before making a brittle assertion.

## Exercise 3: Add A Cart Calculation

Extend the cart tests to check:

```python
cart["total"] == sum(product["total"] for product in cart["products"])
```

Expected outcome:

- use `pytest.approx()` for floating point tolerance
- explain why exact float equality can be brittle

## Exercise 4: Add A Camel Case Request Id Test

Module 14 supports `requestId` in JSON bodies.

Add a test around `extract_request_id()` using:

```json
{
  "requestId": "camel-123"
}
```

Expected outcome:

- the helper returns `"camel-123"`

## Exercise 5: Add CI Schema Scope Discussion

Decide whether the workflow should add a separate `schema` scope.

Answer:

1. Which tests would it run?
2. Would it overlap with `capstone`?
3. When would it be useful?

Expected outcome:

- you can reason about CI scopes without adding unnecessary complexity

## Exercise 6: Compare DummyJSON And JSONPlaceholder

Write a short comparison:

| Area | JSONPlaceholder | DummyJSON |
| --- | --- | --- |
| Auth | ? | ? |
| Nested data | ? | ? |
| Search | ? | ? |
| Capstone suitability | ? | ? |

Expected outcome:

- you can explain why DummyJSON is a better final capstone target

## Exercise 7: Run The Capstone

Run:

```bash
python -m pytest tests/dummyjson -v
```

Expected outcome:

- all capstone tests pass
- you can identify which domain each test file covers
