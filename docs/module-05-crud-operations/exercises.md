# Module 05 Exercises: CRUD Operations

These exercises extend the CRUD method patterns. Use `jsonplaceholder_base_url` and `default_timeout_seconds` in every test.

## Exercise 1: Create A Comment

Create:

```text
tests/learning/test_05_crud/test_comment_create.py
```

Write a test for:

```text
POST /comments
```

Payload:

```python
{
    "postId": 1,
    "name": "Module 05 exercise",
    "email": "module05@example.com",
    "body": "Practicing POST for comments.",
}
```

Expected assertions:

- status code is `201`
- response contains an integer `id`
- response echoes `postId`, `name`, `email`, and `body`

Hint: JSONPlaceholder has 500 comments, so it commonly returns `id: 501` for a created comment.

## Exercise 2: PUT vs PATCH On Users

Create:

```text
tests/learning/test_05_crud/test_user_update.py
```

Write two tests:

1. `PUT /users/1` with a complete user-like payload.
2. `PATCH /users/1` with only `{"email": "changed@example.com"}`.

Expected assertions:

- both return `200`
- PUT response echoes all sent fields
- PATCH response changes the email
- PATCH response still has the same `id`

Hint: if JSONPlaceholder includes fields you did not send, document that observed behavior in a short comment.

## Exercise 3: Delete Then Verify

Write a test that:

1. Sends `DELETE /comments/1`.
2. Asserts status `200`.
3. Asserts the response body is `{}`.
4. Sends `GET /comments/1`.
5. Documents that JSONPlaceholder still returns the original comment because delete is simulated.

Expected outcome:

- The test passes.
- Your comment explains how a real persistent API would usually return `404` after deletion.

## Exercise 4: CRUD Lifecycle For Albums

Create:

```text
tests/learning/test_05_crud/test_album_lifecycle.py
```

Write a simulated lifecycle:

1. `POST /albums` with `{"title": "Exercise album", "userId": 1}`.
2. `GET /albums/1`.
3. `PUT /albums/1` with a new title.
4. `PATCH /albums/1` with another title.
5. `DELETE /albums/1`.

Expected assertions:

- creation returns `201`
- read/update/delete steps return the expected success status
- update responses preserve `id == 1`
- delete returns an empty JSON object

## Exercise 5: Explore Weak Payloads

Write tests to observe JSONPlaceholder behavior for weak write requests:

- `POST /posts` with `data=` instead of `json=`
- `PUT /posts/1` with no body
- `PATCH /posts/1` with `{"notARealField": "value"}`

Expected outcome:

- Your tests assert what JSONPlaceholder actually returns.
- Each test includes a short comment about what a stricter production API might return instead.

## Exercise 6: Explain Idempotency

In your own notes, answer:

1. Why is `GET` idempotent?
2. Why is `PUT` idempotent?
3. Why is `POST` usually not idempotent?
4. Why can DELETE be idempotent even if the second response status differs?
5. What kind of PATCH operation would not be idempotent?

Expected outcome:

- You can explain retry risk for each method before Module 12 discusses resilience in more depth.

