# Markers And Test Selection

## What Markers Do

Markers label tests. Labels let you select the right subset for the moment.

```python
@pytest.mark.smoke
def test_api_health_check(...):
    ...
```

Run smoke tests:

```bash
python -m pytest -m smoke
```

## Registered Project Markers

[`pyproject.toml`](../../pyproject.toml) registers:

| Marker | Purpose |
| --- | --- |
| `smoke` | quick health checks |
| `regression` | broader coverage |
| `crud` | CRUD operation tests |
| `auth` | authentication tests |
| `schema` | schema validation tests |
| `performance` | response-time checks |
| `security` | introductory security checks |
| `e2e` | end-to-end workflows |

Registering markers prevents typo warnings and documents the suite vocabulary.

## Built-In Control Markers

### skip

```python
@pytest.mark.skip(reason="Endpoint not available yet")
def test_v2_endpoint():
    ...
```

The test is collected but not executed.

### skipif

```python
@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_python_310_behavior():
    ...
```

The test runs only when the condition is false.

### xfail

```python
@pytest.mark.xfail(reason="Known bug")
def test_known_bug():
    ...
```

`xfail` means "run it, but a failure is expected."

| Result | Meaning |
| --- | --- |
| `XFAIL` | failed as expected |
| `XPASS` | unexpectedly passed |

Use `strict=True` when an unexpected pass should fail CI.

## Marker Expressions

```bash
python -m pytest -m smoke
python -m pytest -m "crud and not smoke"
python -m pytest -m "smoke or regression"
python -m pytest -m "not (performance or security)"
```

## Keyword Selection

`-k` filters by test node ID and name.

```bash
python -m pytest -k "post and not delete"
```

Use `-m` for categories and `-k` for names.

## Module-Level Markers

Inside a test file:

```python
pytestmark = pytest.mark.regression
```

Every test in that file gets the marker.

## Code References

- [`pyproject.toml`](../../pyproject.toml) registers project markers.
- [`test_markers.py`](../../tests/learning/test_06_pytest_features/test_markers.py) demonstrates skip, xfail, smoke, and regression.
- [`test_smoke.py`](../../tests/learning/test_04_basic_get/test_smoke.py) contains real smoke tests.

## Key Takeaways

- Markers label tests for selection.
- `skip` does not run the test; `xfail` runs it but expects failure.
- Register custom markers in [`pyproject.toml`](../../pyproject.toml).
- Use `-m` for marker expressions and `-k` for name expressions.
