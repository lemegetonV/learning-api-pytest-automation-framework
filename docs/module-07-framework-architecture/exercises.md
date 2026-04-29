# Module 07 Exercises: Framework Architecture

## Exercise 1: Inspect Settings

Run:

```bash
python -c "from src.config import get_settings; print(get_settings())"
```

Expected outcome:

- You see the default base URL.
- Timeout is an integer.
- No `.env` file is required.

## Exercise 2: Override Timeout Locally

Create a local `.env` file from `.env.example`, change:

```env
TEST_TIMEOUT=5
```

Run a short Python command to print `get_settings().timeout`.

Expected outcome:

- It prints `5`.
- `.env` remains untracked by git.

## Exercise 3: Use APIClient Directly

Create a temporary scratch script or run a Python shell:

```python
from src.api_client import APIClient

with APIClient("https://jsonplaceholder.typicode.com") as client:
    response = client.get("/posts/1")
    print(response.status_code)
    print(response.json()["id"])
```

Expected outcome:

- Status is `200`.
- ID is `1`.

## Exercise 4: Add A Client Test

Add a test under `tests/learning/test_07_framework/test_api_client.py` that calls:

```text
GET /users/1
```

Expected assertions:

- status code is `200`
- `id == 1`
- response contains `address`

## Exercise 5: Compare Raw Requests And Client Calls

Find one test in `tests/learning/test_04_basic_get/test_posts.py`.

Write the equivalent using `api_client`.

Expected outcome:

- You can explain which parts disappeared from the test because the framework now owns them.

## Exercise 6: Explain The Layers

In your own notes, answer:

1. What belongs in test files?
2. What belongs in `APIClient`?
3. What belongs in `Settings`?
4. Why should secrets not be committed?
5. Why did we not rewrite all old tests in Module 07?

