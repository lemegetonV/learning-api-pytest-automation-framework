# Module 13 Exercises: CI/CD Integration

## Exercise 1: Read The Workflow

Open `.github/workflows/api-tests.yml`.

Answer:

1. Which events trigger the workflow?
2. Which Python versions does the matrix use?
3. Which command installs dependencies?
4. Which command checks syntax before pytest?

Expected outcome:

- you can explain the CI pipeline without running it

## Exercise 2: Add A Marker Scope

Imagine the project needs a `schema` manual dispatch scope.

Update the workflow case statement to support:

```bash
-m schema
```

Expected outcome:

- `test_workflow_supports_selectable_test_scopes` should be extended to assert `-m schema`
- the workflow should reject unknown scopes

Hint: do not remove existing scopes.

## Exercise 3: Run The CI Contract Tests

Run:

```bash
python -m pytest tests/learning/test_13_cicd -v
```

Expected outcome:

- all CI contract tests pass
- you can explain what workflow behavior each test protects

## Exercise 4: Compare Normal And Parallel Smoke Runs

Run:

```bash
python -m pytest -m smoke -v
python -m pytest -m smoke -n 2 -v
```

Expected outcome:

- both commands pass
- you can describe what xdist changes in the output

## Exercise 5: Explain The Config Isolation Finding

Read `tests/learning/test_07_framework/test_config.py`.

Answer:

1. Why do default settings tests clear environment variables?
2. Why do override tests use `monkeypatch.setenv()`?
3. What kind of CI failure would happen without that isolation?

Expected outcome:

- you understand why environment handling is a CI reliability issue

## Exercise 6: Decide The Right CI Scope

For each situation, choose `full`, `smoke`, `performance`, or `security`:

1. A pull request changes `src/api_client/client.py`.
2. A developer wants a quick health check after JSONPlaceholder was unavailable.
3. A tester is investigating response-time budget examples.
4. A tester is checking token redaction behavior.

Expected outcome:

- you can map CI test scopes to real testing intent

## Exercise 7: Debug A Hypothetical Failure

Suppose CI fails in the `Run pytest` step on a live JSONPlaceholder test, but local mocked tests pass.

Write the first three things you would check.

Expected outcome:

- your answer separates product code failures from public API or CI environment failures
