# Schema Validation vs Business Assertions

Schema validation checks response shape. Business assertions check scenario meaning.

You usually need both.

## Example

This schema validation proves the response looks like a post:

```python
validate_json(post, post_schema)
```

These assertions prove the specific scenario:

```python
assert post["id"] == 1
assert post["userId"] == 1
```

The schema can say `id` is an integer. It cannot know that this test specifically requested `/posts/1` unless the test asserts it.

## Comparison

| Concern | Schema validation | Business assertion |
| --- | --- | --- |
| Field exists | yes | possible but repetitive |
| Field type | yes | possible but repetitive |
| No unexpected fields | yes | awkward manually |
| Requested ID is returned | no | yes |
| Filter only returns requested user | no | yes |
| Error message has expected meaning | partial | yes |

## Good Test Shape

```python
response = api_client.get("/posts/1")
post = response.json()

assert response.status_code == 200
validate_json(post, post_schema)
assert post["id"] == 1
```

The test reads as:

1. The request succeeded.
2. The response body matches the contract.
3. The response matches this scenario.

## What Not To Do

Do not replace all assertions with schema validation.

Do not duplicate the entire schema manually through many `assert isinstance(...)` checks.

Do not validate a response against the wrong schema just because it is convenient.

## Code References

- `tests/learning/test_10_schema/test_contract_boundaries.py`
- `tests/learning/test_10_schema/test_response_schemas.py`

## Key Takeaways

- Schema validation checks contract shape.
- Business assertions check scenario meaning.
- Strong API tests use both.
- A schema is not a substitute for understanding the behavior being tested.
