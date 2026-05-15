# Module 03 Exercises: Environment Setup

These exercises make you prove the environment, not just read about it. Run commands from the project root.

## Exercise 1: Prove You Are Using The Right Python

Run:

```bash
python --version
python -c "import sys; print(sys.executable)"
python -m pip --version
```

Expected outcome:

- Python is 3.10 or newer.
- The executable path points inside `.venv`.
- pip also points inside `.venv`.

Hint: if the path is not inside `.venv`, activate the environment again.

## Exercise 2: Reinstall From The Dependency Recipe

Run:

```bash
python -m pip install -r requirements.txt
python -m pytest --version
python -c "import requests; print(requests.__version__)"
```

Expected outcome:

- pytest is available.
- requests is available.
- The versions match [`requirements.txt`](../../requirements.txt).

Hint: use `python -m pip`, not a standalone `pip`, so the installer belongs to the active Python interpreter.

## Exercise 3: Predict Pytest Discovery

Before running anything, answer which of these pytest will collect:

```text
tests/learning/test_03_environment_setup/test_sample.py::test_valid_name
tests/learning/test_03_environment_setup/sample_test.py::test_valid_name
tests/learning/test_03_environment_setup/test_sample.py::check_valid_name
tests/learning/test_03_environment_setup/test_sample.py::TestExample::test_valid_name
```

Then run:

```bash
python -m pytest --collect-only tests/learning/test_03_environment_setup
```

Expected outcome:

- You can explain why collected tests were found.
- You can explain why incorrectly named files or functions would be ignored.

Hint: compare your answer to `python_files`, `python_classes`, and `python_functions` in [`pyproject.toml`](../../pyproject.toml).

## Exercise 4: Run The Module Tests

Run:

```bash
python -m pytest tests/learning/test_03_environment_setup -v
```

Expected outcome:

- All Module 03 tests pass.
- You can identify which file checks Python, which file checks pytest behavior, and which file checks requests preparation.

Hint: the output includes the full test node id: `path::test_name`.

## Exercise 5: Break One Assertion On Purpose

Temporarily change one assertion in [`test_pytest_behaviour.py`](../../tests/learning/test_03_environment_setup/test_pytest_behaviour.py) so it fails.

Run:

```bash
python -m pytest tests/learning/test_03_environment_setup/test_pytest_behaviour.py -v
```

Observe:

- The test result is `FAILED`, not `ERROR`.
- Pytest shows the assertion expression and values.

Then restore the assertion and rerun the test.

Expected outcome:

- You can explain what pytest showed and why the final run passes again.

## Exercise 6: Inspect A Prepared Request

Open [`test_requests_preparation.py`](../../tests/learning/test_03_environment_setup/test_requests_preparation.py).

Add a new test that prepares a request for:

```text
GET https://jsonplaceholder.typicode.com/comments?postId=1
```

Expected assertions:

- The prepared method is `GET`.
- The prepared URL contains `/comments`.
- The prepared URL contains `postId=1`.

Hint: use `requests.Request(..., params={"postId": 1}).prepare()`.

## Exercise 7: Explain The Setup In Your Own Words

Write short answers for yourself:

1. Why is `.venv/` not committed?
2. Why is [`requirements.txt`](../../requirements.txt) committed?
3. Why do we run `python -m pytest`?
4. What does [`tests/conftest.py`](../../tests/conftest.py) provide?
5. Why does Module 03 avoid live API calls?

Expected outcome:

- You can describe the environment setup without memorizing commands blindly.
