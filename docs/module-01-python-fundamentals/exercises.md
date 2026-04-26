# Module 01 Exercises

These exercises are intentionally small. They are designed to build Python fluency before the project introduces pytest and requests.

## Exercise 1: Name API Values Clearly

Create variables for this imaginary API response:

- status code: `200`
- HTTP method: `"GET"`
- endpoint: `"/posts/1"`
- response time: `0.245`
- response body has JSON: `True`

Print a readable one-line summary.

Hint:

```python
expected_status_code = 200
```

Expected outcome:

- variables have descriptive names
- the printed line clearly tells what request was made and what happened

## Exercise 2: Model A JSON Object

Create a dictionary named `post` with these fields:

- `userId`
- `id`
- `title`
- `body`

Then write assertions that check:

- `id` is `1`
- `title` is a string
- `body` is not empty

Hint:

```python
assert isinstance(post["title"], str)
```

Expected outcome:

- you can represent a JSON object as a Python dictionary
- you can access fields by key

## Exercise 3: Model A JSON Array

Create a list of three post dictionaries. Each post should have `id`, `title`, and `userId`.

Then write code that:

- counts how many posts are in the list
- checks that every post has an `id`
- prints all titles

Hint:

```python
for post in posts:
    print(post["title"])
```

Expected outcome:

- you can represent a JSON array as a Python list
- you can loop through response-like data

## Exercise 4: Spot Type Problems

Given this dictionary:

```python
user = {
    "id": "1",
    "name": "Leanne Graham",
    "active": "true",
}
```

Write checks that reveal which fields have misleading types.

Expected outcome:

- you notice that `"1"` is a string, not an integer
- you notice that `"true"` is a string, not a boolean

## Exercise 5: Explain In Your Own Words

Write short answers:

1. Why is `200` different from `"200"`?
2. Why are dictionaries important for API testing?
3. Why should test variable names be descriptive?

Expected outcome:

- you can explain Python basics in API testing language, not only as syntax rules

## Exercise 6: Response Validator

Write a function named `validate_response_shape(response_body, required_fields)` that:

- accepts a dictionary and a list or set of required field names
- returns a tuple: `(is_valid, missing_fields)`
- uses set operations to detect missing fields
- uses an f-string to print a readable summary

Hint:

```python
expected = set(required_fields)
actual = set(response_body.keys())
missing = expected - actual
```

Expected outcome:

- complete response returns `(True, set())`
- incomplete response returns `(False, {...})`

## Exercise 7: Status Code Classifier

Write a function named `classify_status_code(status_code)` that returns:

- `"success"` for 200-299
- `"client_error"` for 400-499
- `"server_error"` for 500-599
- `"other"` for anything else

Try this once with `if/elif/else`, and optionally again with `match/case`.

Expected outcome:

- `classify_status_code(200)` returns `"success"`
- `classify_status_code(404)` returns `"client_error"`
- `classify_status_code(503)` returns `"server_error"`

## Exercise 8: User Data Analyzer

Given a list of user dictionaries, write code that:

- uses a list comprehension to collect all email addresses
- uses a set to check whether user IDs are unique
- uses a lambda with `sorted()` to sort users by `id`
- handles a missing optional `role` field with `.get()`

Expected outcome:

- you can transform list-of-dictionary API data without mutating the original list

## Exercise 9: Retry Simulator

Write a function named `retry_until_success(results, max_attempts=3)`.

`results` is a list of booleans such as:

```python
[False, False, True]
```

The function should:

- loop through attempts using `range`
- stop early when it sees `True`
- return `True` if a successful attempt happened
- return `False` otherwise
- print attempts using f-strings

Expected outcome:

- `[False, True]` returns `True`
- `[False, False, False]` returns `False`
