# Module 10 Exercises: Schema Validation

## Exercise 1: Read A Schema

Open `schemas/jsonplaceholder/post.schema.json`.

Answer:

1. Which fields are required?
2. Which fields must be integers?
3. What does `additionalProperties: false` mean?

## Exercise 2: Break A Payload Intentionally

Open `tests/learning/test_10_schema/test_schema_helpers.py`.

Change the valid payload in `test_validate_json_accepts_valid_payload` so `id` is `"1"` instead of `1`.

Run:

```bash
python -m pytest tests/learning/test_10_schema/test_schema_helpers.py -v
```

Expected outcome:

- The test fails.
- The error explains that `"1"` is not an integer.

Revert the exercise change after observing the failure.

## Exercise 3: Add A Todo Schema

JSONPlaceholder has `/todos/1`.

Create:

```text
schemas/jsonplaceholder/todo.schema.json
```

Expected fields:

- `userId`
- `id`
- `title`
- `completed`

Hint: `completed` is a boolean.

## Exercise 4: Add A Todo Schema Test

Create a new test in `tests/learning/test_10_schema/test_response_schemas.py`.

Steps:

1. Load your todo schema.
2. Call `GET /todos/1`.
3. Assert status code is `200`.
4. Validate the response JSON.
5. Assert `id == 1`.

## Exercise 5: Explain Format Checking

Read `src/utils/schema_validator.py`.

Answer:

1. Why does the helper use `FormatChecker()`?
2. What could happen if a schema contains `"format": "email"` but the validator is not configured for format checking?

## Exercise 6: Schema Or Business Assertion

For each check, decide whether it belongs in schema validation, a business assertion, or both:

1. Response has an `id` field.
2. `id` is an integer.
3. Response from `/posts/1` has `id == 1`.
4. Unknown field `debug` is not returned.
5. All posts from `GET /posts?userId=1` have `userId == 1`.

Explain your choices.
