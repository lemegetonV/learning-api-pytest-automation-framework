# Schema Files And Validator Helpers

Module 10 keeps schema files and validation mechanics separate from test scenarios.

## File Layout

```text
schemas/
└── jsonplaceholder/
    ├── comment.schema.json
    ├── post.schema.json
    ├── post_collection.schema.json
    └── user.schema.json
```

Tests import helpers from `src/utils/schema_validator.py`:

```python
from src.utils import collect_validation_errors, load_schema, validate_json
```

## Helper Responsibilities

| Helper | Responsibility |
| --- | --- |
| `load_schema(relative_path)` | Load a schema file from the project root |
| `validate_json(data, schema)` | Raise `ValidationError` on the first failure |
| `collect_validation_errors(data, schema)` | Return all failures for analysis |

## Why Helpers Matter

Without helpers, every test would repeat validator setup:

```python
from jsonschema import Draft202012Validator, FormatChecker

validator = Draft202012Validator(schema, format_checker=FormatChecker())
validator.validate(response.json())
```

The framework hides that setup but keeps the test readable:

```python
schema = load_schema("schemas/jsonplaceholder/post.schema.json")
validate_json(response.json(), schema)
```

## Format Checker Nuance

JSON Schema `format` is easy to misunderstand. A schema can say:

```json
{
  "email": {
    "type": "string",
    "format": "email"
  }
}
```

But the Python `jsonschema` library only enforces format rules when the validator is configured with a `FormatChecker`.

Module 10 handles that in `src/utils/schema_validator.py`:

```python
Draft202012Validator(schema, format_checker=FormatChecker())
```

That is why `test_schema_format_checks_need_framework_support` catches invalid email text.

## Code References

- `src/utils/schema_validator.py`
- `src/utils/__init__.py`
- `tests/learning/test_10_schema/test_schema_helpers.py`
- `tests/learning/test_10_schema/test_contract_boundaries.py`

## Key Takeaways

- Tests should not repeat low-level validator setup.
- Use `validate_json()` when one clear failure is enough.
- Use `collect_validation_errors()` when you want richer failure analysis.
- Configure `FormatChecker` if you expect `format` to be enforced.
