# Module 04 Exercises: First API Tests

These exercises extend the GET patterns from the module. Write the code yourself, then run the targeted pytest command.

## Exercise 1: Test The `/todos` Collection

Create:

```text
tests/learning/test_04_basic_get/test_todos.py
```

Write tests for:

- `GET /todos` returns status `200`.
- The body is a list.
- The list contains `200` todos.
- `GET /todos/1` returns a todo with `id == 1`.
- A todo has fields `userId`, `id`, `title`, and `completed`.
- `completed` is a boolean.

Hints:

- Use `jsonplaceholder_base_url` and `default_timeout_seconds`.
- Use `isinstance(todo["completed"], bool)`.
- Keep status assertions before body assertions.

Expected command:

```bash
python -m pytest tests/learning/test_04_basic_get/test_todos.py -v
```

## Exercise 2: Filter Todos By User

In the same `test_todos.py`, add a filter test:

```text
GET /todos?userId=1
```

Expected assertions:

- status code is `200`
- response body is a non-empty list
- every returned todo has `userId == 1`

Hint:

```python
assert all(todo["userId"] == 1 for todo in todos)
```

## Exercise 3: Explore Error Responses

Create:

```text
tests/learning/test_04_basic_get/test_error_responses.py
```

Explore and then test:

- `GET /posts/9999`
- `GET /posts/0`
- `GET /posts/abc`
- `GET /unknown-resource`

Expected outcome:

- You know which status code each route returns.
- Your assertions document observed API behavior.

Hints:

- Do a short exploratory run before finalizing assertions.
- Do not assume every invalid-looking route behaves the same.
- Keep comments brief if you need to explain surprising behavior.

## Exercise 4: Compare Comments Routes

Add a test for post 2 that compares:

```text
GET /posts/2/comments
GET /comments?postId=2
```

Expected assertions:

- both requests return `200`
- both responses are lists
- the sorted comment IDs match

Hint:

```python
nested_ids = sorted(comment["id"] for comment in nested_comments)
filtered_ids = sorted(comment["id"] for comment in filtered_comments)
assert nested_ids == filtered_ids
```

## Exercise 5: Validate User Nested Objects

Add tests for `GET /users/1`:

- `address` is a dictionary.
- `address["geo"]` is a dictionary.
- `geo` contains `lat` and `lng`.
- `company` is a dictionary.
- `company` contains `name`, `catchPhrase`, and `bs`.

Hint: keep top-level and nested object assertions in separate tests so failures are easier to read.

## Exercise 6: Read The Test Report

Run:

```bash
python -m pytest tests/learning/test_04_basic_get -v
```

Answer in your own notes:

1. How many tests ran?
2. Which resources are covered?
3. Which assertions check shape?
4. Which assertions check relationships?
5. Which failures would indicate network or environment issues rather than product bugs?

Expected outcome:

- You can read pytest output as a coverage summary, not just a pass or fail signal.

