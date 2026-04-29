# CRUD Lifecycle And Test Isolation

## Why Chain CRUD Operations

Single-method tests prove each endpoint contract in isolation. A lifecycle test proves that operations can work together.

The ideal persistent CRUD cycle is:

```mermaid
flowchart LR
    A["Create"] --> B["Read created resource"]
    B --> C["Update created resource"]
    C --> D["Read updated resource"]
    D --> E["Delete resource"]
    E --> F["Read returns 404"]
```

## JSONPlaceholder Lifecycle Reality

JSONPlaceholder does not persist writes, so Module 05 cannot perform a true create-read-update-delete cycle against newly created data.

Instead, the lifecycle tests demonstrate the sequence while making assertions that match the fake API:

1. `POST /posts` returns `201` and an `id`.
2. `GET /posts/1` demonstrates read behavior against existing data.
3. `PUT /posts/1` returns an updated-looking response.
4. `PATCH /posts/1` returns a patched-looking response.
5. `DELETE /posts/1` returns `200` and `{}`.

The test comments explain where a real persistent API would assert more.

## Request Chaining

Request chaining means one response provides data for the next request.

Example:

```python
create_response = requests.post(url, json=payload, timeout=10)
created = create_response.json()
post_id = created["id"]

delete_response = requests.delete(
    f"{jsonplaceholder_base_url}/posts/{post_id}",
    timeout=default_timeout_seconds,
)
```

In real APIs, this lets tests operate on data they created themselves. That improves isolation.

## Test Isolation

Each test should be able to run alone.

Good:

```python
def test_update_post():
    payload = {"title": "Updated", "body": "Body", "userId": 1}
    response = requests.put(
        f"{jsonplaceholder_base_url}/posts/1",
        json=payload,
        timeout=default_timeout_seconds,
    )
    assert response.status_code == 200
```

Bad:

```python
created_id = None

def test_create_post():
    global created_id
    created_id = create_response.json()["id"]

def test_update_created_post():
    response = requests.put(f"{jsonplaceholder_base_url}/posts/{created_id}", ...)
```

The second test depends on another test running first. That becomes fragile and breaks parallel execution.

## Cleanup Thinking

For a real API, a create test should have a cleanup strategy.

Options:

- delete the resource at the end of the test
- use fixtures with teardown
- use unique test data and scheduled cleanup
- use a sandbox environment that can be reset

Module 06 introduces pytest fixtures more deeply. Module 09 introduces stronger test data strategy.

## Simulated vs Persistent CRUD

| Question | JSONPlaceholder | Persistent API |
| --- | --- | --- |
| Does `POST` return success? | yes | should, for valid payloads |
| Can you `GET` the new ID? | no | yes |
| Does `PUT` change future `GET` output? | no | yes |
| Does `DELETE` remove the resource? | no | yes |
| Is it still useful for learning requests? | yes | yes |

The key is to avoid writing false assertions. A test should document what the target API actually does.

## Code References

- `tests/learning/test_05_crud/test_crud_lifecycle.py::test_simulated_crud_lifecycle_documents_each_step`
- `tests/learning/test_05_crud/test_crud_lifecycle.py::test_create_then_delete_created_id_documents_fake_persistence`
- `tests/learning/test_05_crud/test_crud_lifecycle.py::test_multiple_patch_responses_are_independent_with_fake_persistence`

## Key Takeaways

- Lifecycle tests verify workflows, not only endpoints.
- Request chaining is a core API testing skill.
- Tests should not depend on other tests.
- Real write tests need cleanup strategy.
- JSONPlaceholder teaches request/response patterns but not real persistence.
