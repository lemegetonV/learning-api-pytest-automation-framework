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
