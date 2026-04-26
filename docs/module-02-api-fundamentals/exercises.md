# Module 02 Exercises

These exercises are concept-first. You do not need pytest or requests yet. Use your browser, API documentation pages, notes, and small tables.

## Exercise 1: Map The Request/Response Cycle

Pick this URL:

```text
https://jsonplaceholder.typicode.com/posts/1
```

Write down:

- method
- base URL
- endpoint path
- path parameter, if any
- expected status code
- likely response body fields
- at least three assertions you would automate later

Expected outcome:

- you can break one API call into request and response parts

## Exercise 2: Status Code Detective

For each scenario, choose the most likely status code and explain why:

| Scenario | Your Status Code |
|---|---|
| resource was fetched successfully | |
| resource was created successfully | |
| request body is malformed | |
| auth token is missing | |
| user is logged in but lacks permission | |
| resource does not exist | |
| too many requests were sent | |
| server dependency is down | |

Expected outcome:

- you can distinguish `401`, `403`, `404`, `429`, and `5xx`

## Exercise 3: Method Selection

Choose the best HTTP method:

| User Goal | Method |
|---|---|
| get a list of users | |
| create a new post | |
| replace an entire user profile | |
| update only a user's email | |
| remove a product | |
| check which methods an endpoint allows | |

Expected outcome:

- you can map CRUD behavior to HTTP methods

## Exercise 4: REST vs SOAP vs GraphQL

For each situation, pick the API style that seems most likely and explain your reasoning:

1. A banking integration uses XML envelopes and a WSDL.
2. A frontend wants to request only `id`, `name`, and `price` from a product object.
3. A public fake API exposes `/posts`, `/posts/1`, and `/comments`.
4. A service uses Protocol Buffers and generated clients.
5. A chat app keeps a connection open for real-time messages.

Expected outcome:

- you can recognize major API styles and connect them to testing approaches

## Exercise 5: Versioning Risk Analysis

Imagine an API changes from `/v1/users` to `/v2/users`.

Write a small risk list for these changes:

- `name` becomes `fullName`
- `id` changes from integer to string
- a new optional `role` field is added
- old `/v1/users` endpoint still exists but returns a deprecation header

Expected outcome:

- you can identify breaking vs non-breaking changes
- you can propose compatibility tests

## Exercise 6: API Documentation Audit

Open the JSONPlaceholder docs and DummyJSON docs in your browser.

For each API, write:

- base URL
- one list endpoint
- one detail endpoint
- whether auth is required
- whether pagination exists
- one positive test idea
- one negative test idea
- one documentation gap or question

Expected outcome:

- you can inspect docs and convert them into test ideas

## Exercise 7: Auth Scenario Matrix

Create a table for a protected endpoint:

| Scenario | Expected Status | Why |
|---|---|---|
| no token | | |
| malformed token | | |
| expired token | | |
| valid token but wrong role | | |
| valid token and correct role | | |

Expected outcome:

- you can explain authentication vs authorization using `401` and `403`

## Exercise 8: Build A Test Matrix

Choose one endpoint from DummyJSON, such as:

```text
GET /products/search?q=phone
```

Create a test matrix with at least:

- 2 happy-path tests
- 2 negative tests
- 2 boundary or edge tests
- 1 pagination/search/sort-related test

Expected outcome:

- you can turn endpoint documentation into structured test coverage

## How To Check Your Work

Your answers should show:

- correct use of HTTP vocabulary
- clear distinction between request and response parts
- correct status-code reasoning
- awareness of auth and versioning risks
- test ideas that can later become pytest tests
