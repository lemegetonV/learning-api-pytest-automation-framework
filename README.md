# API Testing Framework — Python + Pytest + Requests

Clean module-by-module API test automation framework for learning Python, pytest, requests, framework architecture, CI, reporting, and an E2E API capstone.

## Status
This repository is being rebuilt from scratch after archiving the previous completed 15-module implementation. The rebuild keeps the same linear learning model but improves the docs, diagrams, structure, and topic placement.

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v
```

## Test Targets
- JSONPlaceholder for core REST learning modules
- httpbin for selected request/auth behavior examples
- DummyJSON for the final capstone suite
- FakeStore only as optional comparison/practice

## Learning Layout
- `docs/` contains module-by-module learning guides
- `tests/learning/` contains tutorial tests grouped by module
- `tests/dummyjson/` contains the production-style capstone suite
- `src/` contains reusable framework code introduced incrementally
