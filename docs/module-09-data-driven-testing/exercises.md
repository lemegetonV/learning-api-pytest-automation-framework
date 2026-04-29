# Module 09 Exercises: Data-Driven Testing

## Exercise 1: Read The Data Files

Open:

- `test-data/module_09/post_payloads.json`
- `test-data/module_09/post_filters.csv`

Answer:

1. Which file is better for nested payload data?
2. Which file is easier to read as a table?
3. Why does the CSV test convert values with `int(...)`?

## Exercise 2: Add A JSON Payload Case

Add one new object to `test-data/module_09/post_payloads.json`.

Expected fields:

- `case_id`
- `payload`
- `expected_status`

Run:

```bash
python -m pytest tests/learning/test_09_data_driven/test_static_file_data.py -v
```

Expected outcome:

- Pytest shows your `case_id` in the test output.
- The POST test sends your payload.
- JSONPlaceholder returns `201`.

## Exercise 3: Add A CSV Filter Row

Add this row to `test-data/module_09/post_filters.csv`:

```csv
second-user-posts,2,10
```

Run the static data test again.

Expected outcome:

- A new parameterized case appears.
- The test converts `"2"` and `"10"` into integers before using them.

## Exercise 4: Compare Seeds

Run a Python shell:

```python
from tests.learning.test_09_data_driven.test_generated_data import build_fake_post_payload

print(build_fake_post_payload(seed=2026))
print(build_fake_post_payload(seed=2026))
print(build_fake_post_payload(seed=2027))
```

Expected outcome:

- The first two payloads match.
- The third payload differs.

## Exercise 5: Decide The Data Source

For each scenario, choose inline data, JSON, CSV, or Faker:

1. Three post IDs: `1`, `50`, `100`
2. A complex checkout payload with nested items
3. A table of query filters and expected counts
4. Random-looking user names for profile creation

Explain your choices.

## Exercise 6: Explain The Strategy

In your own notes, answer:

1. What belongs in `test-data/`?
2. What belongs in `src/utils/data_loader.py`?
3. Why should generated data be seeded in CI?
4. Why is Module 10 the right place for schema validation instead of Module 09?
