# Loading JSON And CSV Data

Module 09 adds a small loader in `src/utils/data_loader.py` so tests can read files from the project root without hard-coding absolute paths.

## Loader Functions

```python
def project_path(relative_path: str) -> Path:
    return PROJECT_ROOT / relative_path


def load_json_data(relative_path: str) -> Any:
    with project_path(relative_path).open(encoding="utf-8") as data_file:
        return json.load(data_file)


def load_csv_data(relative_path: str) -> list[dict[str, str]]:
    with project_path(relative_path).open(newline="", encoding="utf-8") as data_file:
        return list(csv.DictReader(data_file))
```

## Why Project-Relative Paths

Tests may run from different working directories:

```bash
python -m pytest tests/ -v
python -m pytest tests/learning/test_09_data_driven -v
```

Using `project_path("test-data/module_09/post_payloads.json")` keeps data lookup consistent.

## JSON Data

`test-data/module_09/post_payloads.json` contains POST request cases:

```json
{
  "case_id": "complete-post",
  "payload": {
    "title": "Module 09 data-driven post",
    "body": "This payload is stored in JSON so the test logic stays small.",
    "userId": 1
  },
  "expected_status": 201
}
```

JSON is good for API payloads because it keeps:

- objects
- arrays
- strings
- numbers
- booleans
- nulls

## CSV Data

`test-data/module_09/post_filters.csv` contains query examples:

```csv
case_id,user_id,expected_count
first-user-posts,1,10
middle-user-posts,5,10
last-user-posts,10,10
```

CSV is useful for simple rows, but every value loads as text. That is why the test converts:

```python
user_id = int(row["user_id"])
expected_count = int(row["expected_count"])
```

## JSON vs CSV

| Need | Prefer |
| --- | --- |
| Nested payloads | JSON |
| Numeric and boolean types preserved | JSON |
| Human-editable table | CSV |
| Spreadsheet-friendly data | CSV |
| Complex API request bodies | JSON |

## Code References

- `src/utils/data_loader.py`
- `src/utils/__init__.py`
- `tests/learning/test_09_data_driven/test_data_loader.py`
- `tests/learning/test_09_data_driven/test_static_file_data.py`

## Key Takeaways

- Load data through one helper instead of repeating file-open logic.
- JSON is usually the best fit for API payloads.
- CSV is useful for table-shaped examples.
- Convert CSV values intentionally before using them in API calls.
