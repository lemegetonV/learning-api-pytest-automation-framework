# Module 14 Exercises: Reporting

## Exercise 1: Generate An HTML Report

Run:

```bash
python -m pytest tests/learning/test_14_reporting \
  --html=reports/module-14-report.html \
  --self-contained-html
```

Expected outcome:

- tests pass
- an HTML report is generated under `reports/`

## Exercise 2: Generate Allure Result Files

Run:

```bash
python -m pytest tests/learning/test_14_reporting \
  --alluredir=reports/allure-results
```

Expected outcome:

- tests pass
- raw Allure result files are generated under `reports/allure-results`

## Exercise 3: Add A Request Id Case

Open `tests/learning/test_14_reporting/test_safe_report_context.py`.

Add a test where the response body contains:

```json
{
  "requestId": "camel-123"
}
```

Expected outcome:

- `extract_request_id(response)` returns `"camel-123"`

## Exercise 4: Add A New Sensitive Query Name

Open `src/utils/security.py`.

Add `session_id` to the sensitive query parameter names.

Expected outcome:

- a URL such as `https://service.test/profile?session_id=abc123` is redacted before entering report context

## Exercise 5: Explain Report Types

Answer:

1. What is `pytest-html` best for?
2. What is JUnit XML best for?
3. What does `allure-pytest` generate?
4. Why is the Allure CLI not required in this module?

Expected outcome:

- you can explain which report format solves which problem

## Exercise 6: Debug A Failed CI Run

Imagine a CI run fails on a schema test.

Use the Module 14 artifact strategy to answer:

1. Which artifact would you open first for a human-readable summary?
2. Which file would a CI dashboard parse?
3. Which field in safe report context helps backend teams search logs?

Expected outcome:

- you can connect reports to real failure analysis

## Exercise 7: Check Logs With Caplog

Read `tests/learning/test_14_reporting/test_logging_output.py`.

Add an assertion that the logged URL contains `/health`.

Expected outcome:

- you understand how `caplog` captures framework logs during a test
