# Test Organization, Classes, And Layout

## Functions Are Still Fine

Modules 04 and 05 use standalone test functions. That is a good default for clear API tests.

Classes become useful when a file has natural groups:

- happy path
- validation
- negative behavior
- one resource family

## Test Classes

```python
class TestPostRetrieval:
    def test_get_single_post(self, jsonplaceholder_base_url):
        ...
```

Rules:

- class name starts with `Test`
- method names start with `test_`
- do not define `__init__`
- fixtures are still injected by parameter name

## Do Not Share Mutable State Through `self`

Avoid this:

```python
class TestBadState:
    def test_create(self):
        self.post_id = 101

    def test_update(self):
        assert self.post_id == 101
```

Tests must be independent. Execution order is not a contract. Use fixtures instead.

## Class-Level Markers

```python
@pytest.mark.regression
class TestPostValidation:
    ...
```

Every test method in the class receives the marker.

## Class Autouse Fixtures

Autouse fixtures can set up data for every method in a class.

```python
class TestUserShape:
    @pytest.fixture(autouse=True)
    def fetch_user(self, api_session):
        response = api_session.get(f"{api_session.base_url}/users/1")
        self.user = response.json()
```

This is acceptable for read-only data used by several tests. Avoid it for hidden mutation.

## Layout Direction For This Project

Current learning tests are module-oriented:

```text
tests/learning/test_04_basic_get/
tests/learning/test_05_crud/
tests/learning/test_06_pytest_features/
```

Later production-style capstone tests will be domain-oriented:

```text
tests/dummyjson/products/
tests/dummyjson/auth/
tests/dummyjson/carts/
```

The learning lane teaches concepts. The capstone lane will look more like a production suite.

## Code References

- `tests/learning/test_06_pytest_features/test_classes.py`
- `tests/learning/test_04_basic_get/test_posts.py`
- `tests/learning/test_05_crud/test_crud_lifecycle.py`

## Key Takeaways

- Use functions first.
- Use classes for natural grouping, not shared mutable state.
- Fixtures still work inside classes.
- Class markers apply to all methods.
- Keep learning tests module-oriented until the capstone.

