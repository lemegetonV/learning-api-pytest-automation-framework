# Module 06 Exercises: Pytest Deep Dive

## Exercise 1: Add A Local Fixture

In `tests/learning/test_06_pytest_features/conftest.py`, add a fixture named `known_post`.

It should return:

```python
{"id": 1, "userId": 1, "title": "example", "body": "example"}
```

Write one test that uses it and asserts the keys.

Expected outcome:

- You can explain why the fixture is visible only in the Module 06 directory and below.

## Exercise 2: Parametrize More Endpoints

Add a parametrized test for:

```text
/albums -> 100
/photos -> 5000
/todos -> 200
```

Expected assertions:

- response status is `200`
- response body length matches the expected count

Hint: use one test function with `@pytest.mark.parametrize`.

## Exercise 3: Add Custom IDs

Rewrite one parametrized test using `pytest.param(..., id="...")`.

Expected outcome:

- The pytest output has readable names instead of raw values only.

## Exercise 4: Marker Selection

Run:

```bash
python -m pytest tests/learning/test_06_pytest_features -m smoke -v
python -m pytest tests/learning/test_06_pytest_features -m regression -v
python -m pytest tests/learning/test_06_pytest_features -k "post" -v
```

Expected outcome:

- You can explain why each command selected the tests it selected.

## Exercise 5: Create A Test Class

Create a class named `TestTodoValidation`.

Add methods for:

- `GET /todos/1` returns status `200`
- `id` is an integer
- `completed` is a boolean
- `title` is a non-empty string

Expected outcome:

- The tests are grouped under the class in verbose pytest output.

## Exercise 6: Explain skip vs xfail

In your own notes, answer:

1. When should a test be skipped?
2. When should a test be marked xfail?
3. Why can xfail be better than deleting a test for a known bug?
4. What does XPASS mean?

