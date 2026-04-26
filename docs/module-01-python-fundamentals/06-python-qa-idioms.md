# Python QA Idioms And Supplemental Concepts

## Why This Guide Exists

The first five guides teach the core Python building blocks. This supplemental guide covers the Python idioms that show up constantly in test automation code, examples, framework helpers, and debugging.

You do not need to memorize every pattern immediately. You should be able to recognize them when they appear later.

## Naming Rules And Conventions

Python variable and function names should be descriptive and use `snake_case`.

```python
base_url = "https://jsonplaceholder.typicode.com"
max_retry_count = 3
expected_status_code = 200
```

Rules:

| Rule | Good | Bad |
|---|---|---|
| starts with letter or underscore | `status_code` | `200_status` |
| no spaces | `response_time` | `response time` |
| not a Python keyword | `user_class` | `class` |
| use descriptive names | `expected_status_code` | `x` |

In test automation, clear names reduce debugging time.

## F-Strings

F-strings are Python's modern string-formatting tool.

```python
endpoint = "/posts/1"
status_code = 404

message = f"Expected 200 for {endpoint}, got {status_code}"
```

They are used for readable assertion messages, URLs, logs, and generated test-case labels.

```python
base_url = "https://api.example.com"
resource = "posts"
post_id = 1

url = f"{base_url}/{resource}/{post_id}"
assert url == "https://api.example.com/posts/1"
```

Prefer f-strings over manual concatenation:

```python
# Avoid
message = "Expected 200, got " + str(status_code)

# Prefer
message = f"Expected 200, got {status_code}"
```

## Checking Types With `type()` And `isinstance()`

`type()` tells you the exact type:

```python
print(type(200))       # <class 'int'>
print(type("200"))     # <class 'str'>
```

For assertions, `isinstance()` is usually better:

```python
post = {"id": 1, "title": "hello"}

assert isinstance(post["id"], int)
assert isinstance(post["title"], str)
```

`isinstance()` communicates the test intent: this field should behave like this type.

## Type Casting

Type casting converts a value from one type to another.

```python
status_as_text = "200"
status_code = int(status_as_text)

assert status_code == 200
```

Common casts:

```python
int("10")       # 10
float("9.99")   # 9.99
str(200)        # "200"
bool(1)         # True
```

Be careful: casting invalid values raises errors.

```python
int("abc")  # ValueError
```

## Truthy And Falsy Values

Python treats some values as false in conditions.

Falsy values:

```python
False
None
0
0.0
""
[]
{}
set()
```

Truthy values:

```python
True
1
"hello"
[1]
{"id": 1}
```

API testing example:

```python
response_body = {"title": ""}

if not response_body["title"]:
    print("title is empty")
```

Use this carefully. Sometimes you need to distinguish missing, empty, and zero values.

## `is` vs `==`

Use `==` for value equality.

```python
assert status_code == 200
assert title == "hello"
```

Use `is` for identity checks, especially `None`.

```python
value = None

assert value is None
assert value is not False
```

Prefer `value is None` over `value == None`.

## `range()`

`range()` creates a sequence of numbers, commonly used in loops.

```python
for attempt in range(3):
    print(f"Attempt {attempt + 1}")
```

Forms:

```python
range(3)        # 0, 1, 2
range(1, 4)     # 1, 2, 3
range(0, 10, 2) # 0, 2, 4, 6, 8
```

QA use cases include retry attempts, pagination offsets, and generated test IDs.

## Ternary Expressions

A ternary expression is a compact `if/else` for assigning one value.

```python
status_code = 201
result = "pass" if status_code in [200, 201] else "fail"
```

Use it only when it stays readable. For multi-step decisions, use normal `if/elif/else`.

## Loop `else`

Python loops can have an `else` block. It runs only if the loop finishes without `break`.

```python
status_codes = [200, 200, 201]

for status_code in status_codes:
    if status_code >= 500:
        print("server failure found")
        break
else:
    print("no server failures found")
```

This is useful for "search until found" patterns, but many teams avoid it because it is less familiar. Use it only when your team finds it clear.

## `match` / `case`

`match` / `case` is structural pattern matching, available in Python 3.10+.

```python
status_code = 404

match status_code:
    case 200:
        category = "ok"
    case 201:
        category = "created"
    case 404:
        category = "not_found"
    case _:
        category = "other"
```

It can make classification logic readable. For basic conditions, `if/elif/else` is still fine.

## `*args`

`*args` collects extra positional arguments into a tuple.

```python
def run_named_checks(*check_names):
    for check_name in check_names:
        print(f"Running {check_name}")

run_named_checks("status", "headers", "body")
```

You will not need `*args` often as a beginner, but you may see it in libraries and framework hooks.

## `**kwargs`

`**kwargs` collects extra keyword arguments into a dictionary.

```python
def build_post(**overrides):
    payload = {
        "title": "default title",
        "body": "default body",
        "userId": 1,
    }
    payload.update(overrides)
    return payload

payload = build_post(title="custom")
```

This pattern becomes central in Module 09 data factories.

## Lambda Functions

A lambda is a small anonymous function.

```python
response_times = [
    {"endpoint": "/posts", "time": 0.30},
    {"endpoint": "/users", "time": 0.12},
]

sorted_times = sorted(response_times, key=lambda item: item["time"])
```

Use lambdas for short expressions, especially sorting or filtering. If the logic needs explanation, write a normal function.

## Docstrings

A docstring explains what a function, class, or module does.

```python
def status_category(status_code):
    """Return a broad HTTP status category for a status code."""
    if 200 <= status_code < 300:
        return "success"
    if 400 <= status_code < 500:
        return "client_error"
    if 500 <= status_code < 600:
        return "server_error"
    return "other"
```

Framework helpers should have useful docstrings when their behavior is not obvious from the name.

## Slicing

Slicing extracts part of a list or string.

```python
endpoints = ["/posts", "/comments", "/users", "/todos"]

first_two = endpoints[:2]
middle = endpoints[1:3]
last = endpoints[-1]
```

| Expression | Meaning |
|---|---|
| `items[:2]` | from start up to index 2, excluding 2 |
| `items[1:3]` | index 1 up to index 3, excluding 3 |
| `items[-1]` | last item |

API use case: sampling the first few records in a response.

## More List Operations

```python
endpoints = ["/posts"]

endpoints.append("/users")
endpoints.extend(["/comments", "/todos"])

assert "/users" in endpoints
assert len(endpoints) == 4
```

Common operations:

| Operation | Purpose |
|---|---|
| `append` | add one item |
| `extend` | add many items |
| `remove` | remove by value |
| `pop` | remove and return by position |
| `sort` | sort in place |
| `sorted` | return a sorted copy |

## Dictionary Update And Pop

```python
payload = {"title": "old", "userId": 1}

payload.update({"title": "new"})
title = payload.pop("title")
missing_role = payload.pop("role", None)
```

`update()` is useful when overriding defaults. `pop()` is useful when removing optional fields for negative tests.

## Comprehensions

Comprehensions build collections concisely.

```python
users = [
    {"id": 1, "active": True},
    {"id": 2, "active": False},
]

active_user_ids = [user["id"] for user in users if user["active"]]
headers = ["Content-Type", "Accept"]
normalized = {header.lower(): header for header in headers}
user_ids = {user["id"] for user in users}
```

Use comprehensions for simple transformations. Use normal loops when the logic needs multiple steps or clearer failure messages.

## Set Operations

Sets are useful for comparing expected and actual fields.

```python
expected_fields = {"id", "title", "body", "userId"}
actual_fields = {"id", "title", "body"}

missing_fields = expected_fields - actual_fields
extra_fields = actual_fields - expected_fields

assert missing_fields == {"userId"}
assert extra_fields == set()
```

This pattern appears often in response-shape validation before formal JSON Schema is introduced.

## Custom Exceptions

Custom exceptions give domain-specific names to failure categories.

```python
class APIError(Exception):
    """Base error for API helper failures."""


class AuthenticationError(APIError):
    """Raised when authentication fails."""


def require_token(token):
    if not token:
        raise AuthenticationError("Missing auth token")
```

You will not need custom exceptions in the earliest modules, but they are useful in larger framework utilities.

## Reading Tracebacks

A traceback tells you what exception happened, where it happened, and which calls led there.

Read from the bottom first:

```text
KeyError: 'title'
```

Then look at the file and line above it. That is usually the line where your code made the bad lookup.

## Debugging Mindset

When Python fails:

1. Read the exception type.
2. Read the exact line number.
3. Check the value and type involved.
4. Ask whether this is a test bug, expected negative behavior, or system behavior.

Good API testing depends on diagnosing failures accurately.

## Key Takeaways

- F-strings are the default way to build readable messages and URLs.
- `type()`, `isinstance()`, and type casting help explain data mismatches.
- Truthy/falsy checks are concise, but they can hide differences between empty, missing, and zero.
- Comprehensions and set operations are powerful for response validation when kept readable.
- Tracebacks are debugging tools, not noise.
