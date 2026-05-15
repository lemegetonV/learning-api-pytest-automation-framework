# Generated Data With Faker

Static files are not the only data source. Sometimes tests need realistic values without hand-writing every title, paragraph, email, or address.

Module 09 activates `faker` in [`requirements.txt`](../../requirements.txt).

## Why Generate Data

Generated data is useful when:

- the exact text does not matter
- realistic shape matters
- repeated hard-coded strings make tests noisy
- you want more variety than a static file provides

Generated data is risky when it is random and cannot be reproduced. That is why Module 09 uses seeds.

## Seeded Generation

[`test_generated_data.py`](../../tests/learning/test_09_data_driven/test_generated_data.py) uses:

```python
def build_fake_post_payload(seed: int, user_id: int = 1) -> dict[str, object]:
    fake = Faker()
    fake.seed_instance(seed)
    return {
        "title": fake.sentence(nb_words=6).rstrip("."),
        "body": fake.paragraph(nb_sentences=2),
        "userId": user_id,
    }
```

The seed makes the output repeatable:

```python
first_payload = build_fake_post_payload(seed=2026, user_id=3)
second_payload = build_fake_post_payload(seed=2026, user_id=3)

assert first_payload == second_payload
```

## Deterministic vs Generated

| Data type | Strength | Risk |
| --- | --- | --- |
| Fixed data | Easy to read and debug | Can become repetitive or unrealistic |
| Unseeded generated data | High variety | Failures may be hard to reproduce |
| Seeded generated data | Realistic and reproducible | Still needs clear constraints |

## Generated Data Still Needs A Contract

The generated payload test still asserts the API contract:

```python
assert response.status_code == 201
assert body["title"] == payload["title"]
assert body["body"] == payload["body"]
assert body["userId"] == user_id
```

Faker does not replace assertions. It only supplies input data.

## Practical Rule

Use fixed data when the exact value matters. Use seeded generated data when realistic variety matters. Avoid unseeded random data in a learning or CI suite unless there is a strong reason and excellent failure logging.

## Code References

- [`requirements.txt`](../../requirements.txt)
- [`test_generated_data.py`](../../tests/learning/test_09_data_driven/test_generated_data.py)

## Key Takeaways

- Faker helps create realistic data.
- Seeds make generated data reproducible.
- Generated data must still satisfy the API request contract.
- More randomness is not automatically better test coverage.
