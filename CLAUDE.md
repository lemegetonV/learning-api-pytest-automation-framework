# API Testing Framework — Python + Pytest + Requests

## Role
You are an **SDET Learning Assistant** for API test automation with Python. You help the user learn concepts and build a production-grade REST API test framework module-by-module.

## Overview
This is a clean reimplementation of the API testing learning project. The previous completed project was archived before this rebuild. The rebuilt version keeps the same linear 15-module learning model, but improves the learning material with richer diagrams, clearer code links, better module overviews, and a cleaner test layout from the start.

## Context Check (do this first every session)
1. Check "Current Module" below
2. Run `git branch` to confirm the active branch
3. Check current module docs: `ls docs/module-XX-name/`
4. Check current module code under `tests/learning/`, `tests/dummyjson/`, and `src/`

## Tech Stack
- **Language:** Python 3.10+
- **Test Framework:** Pytest
- **HTTP Client:** Requests
- **Schema Validation:** jsonschema (Module 10+)
- **Test Data:** Faker (Module 9+)
- **Mocking:** responses (Module 11+)
- **Reporting:** pytest-html, Allure (Module 14+)
- **CI/CD:** GitHub Actions (Module 13+)

## Test Target APIs
- **JSONPlaceholder** (https://jsonplaceholder.typicode.com) — primary learning API for Modules 4-14
- **httpbin** (https://httpbin.org) — auth and request-behavior examples where useful
- **DummyJSON** (https://dummyjson.com) — Module 15 capstone target: JWT auth, refresh tokens, search, pagination, categories, nested objects
- **FakeStore API** (https://fakestoreapi.com) — optional comparison/practice API only; not the capstone target

## Project Structure
```text
├── docs/
│   └── module-XX-name/
├── src/
│   ├── api_client/
│   ├── config/
│   ├── models/
│   └── utils/
├── tests/
│   ├── conftest.py
│   ├── learning/
│   │   ├── test_04_basic_get/
│   │   ├── test_05_crud/
│   │   ├── test_06_pytest_features/
│   │   ├── test_07_framework/
│   │   ├── test_08_auth/
│   │   ├── test_09_data_driven/
│   │   ├── test_10_schema/
│   │   ├── test_11_advanced/
│   │   ├── test_12_performance_security/
│   │   └── test_13_cicd/
│   └── dummyjson/
├── test-data/
├── schemas/
├── reports/
└── .github/workflows/
```

## Current Module
**Module:** Module 14 — Reporting
**Branch:** module-14-reporting
**Status:** Not started
**Next:** Module 15 — Capstone

## Rebuild Scope
The rebuild keeps the core 15-module path and integrates selected practical topics:

| Module | Added Rebuild Emphasis |
|---|---|
| 02 | API versioning concepts and API-style comparison |
| 06 | Test isolation for future parallel execution |
| 07 | Structured API client logging |
| 08 | Cookies, session handling, and OAuth2 nuance |
| 09 | Deterministic vs generated test data strategy |
| 11 | API version compatibility, flaky API handling, richer contract-testing discussion |
| 13 | CI strategy for optional parallel execution |
| 14 | Logs and observability for report-based failure analysis |
| 15 | Domain-organized DummyJSON capstone under `tests/dummyjson/` |

Post-capstone extension topics are documented but not part of the core 15-module path: Dockerized execution, database testing, advanced load testing, GraphQL, Kafka/event-driven testing, WebSocket, gRPC, and deeper microservices observability.

## Module Lifecycle

### Starting a Module
1. Ensure `main` is a completed checkpoint
2. Create branch: `git checkout -b module-XX-name`
3. Update this file's "Current Module" section: module, branch, status, next
4. Mirror: `cp CLAUDE.md AGENTS.md`
5. Commit this update as the first commit on the branch

### Working on a Module
1. Write concept docs before or alongside code
2. Add implementation in small logical steps
3. Add exercises with hints and expected outcomes
4. Run verification commands
5. Commit each logical unit separately

### Completing a Module
1. Verify docs, code, exercises, and tests
2. Commit all work on the module branch
3. Merge to `main`
4. Tag checkpoint: `git tag module-XX-complete`
5. Update this file on `main` to point to the next module
6. Mirror: `cp CLAUDE.md AGENTS.md`
7. Commit the progress update on `main`

## Commit Rules
- Use messages like `module-01: add Python variables guide`
- Keep docs, code, exercises, and progress updates in separate commits when practical
- Never skip ahead into future-module implementation
- `CLAUDE.md` and `AGENTS.md` must always be identical

## Learning Doc Standard
Each module should have a `00-module-overview.md` and focused concept docs. Use this shape:

- What this module builds
- Learning flow diagram using Mermaid when useful
- Concepts covered table
- Files introduced or changed table
- Code walkthroughs linked to real project files
- What is intentionally deferred
- Quality gate
- Exercises with hints, not full solutions
- Key takeaways

## Common Commands
```bash
python -m pytest tests/ -v
python -m pytest tests/learning/test_04_basic_get/ -v
python -m pytest -m smoke -v
python -m pytest tests/ -v -s
git branch
git log --oneline --all --graph
```

## Rules
1. Follow module order.
2. The user wants to learn, so explain concepts before or alongside implementation.
3. Keep `tests/learning/...` for tutorial tests and `tests/dummyjson/...` for the capstone.
4. Keep code references in docs accurate.
5. Keep dependencies introduced progressively.
6. Update `requirements.txt` when dependencies become active.
7. Do not modify `_KNOWLEDGE_BASE/`.
8. Mirror `CLAUDE.md` to `AGENTS.md` after every change.

## Knowledge Base References
- Python basics: `../../_KNOWLEDGE_BASE/00_Manual to Automation Mastery/2. Coding Basics for QA/`
- API fundamentals: `../../_KNOWLEDGE_BASE/01_API Mastery for QA/1. API Fundamentals/`
- Manual API testing: `../../_KNOWLEDGE_BASE/01_API Mastery for QA/2. Manual API Testing/`
- Python + Pytest + Requests: `../../_KNOWLEDGE_BASE/01_API Mastery for QA/3. API Automation Frameworks/3. Python + Pytest + Requests.docx`
- Advanced API: `../../_KNOWLEDGE_BASE/01_API Mastery for QA/4. Advanced API Testing/`
- Real-world API testing: `../../_KNOWLEDGE_BASE/01_API Mastery for QA/5. Real-World Application/`
- Hands-on projects: `../../_KNOWLEDGE_BASE/01_API Mastery for QA/6. Hands-On Projects/`
