# Tests README

This directory contains the automated test suite for the FastAPI Notes API.

## How to run tests

From the project root:

```
python -m pytest -q
```

Run a specific file:

```
python -m pytest tests/test_notes_api.py -q
python -m pytest tests/test_notes.py -q
```

Run a specific test function (node id):

```
python -m pytest tests/test_notes_api.py::test_create_note_success -q
```

Tip: Running from inside this `tests/` folder also works:

```
cd tests
python -m pytest -q
```

## What gets tested

- `test_notes_api.py`: Comprehensive API coverage
  - Create, Read (list + single), Update (partial), Delete
  - Validation failures (missing fields, invalid date, wrong types)
  - Error handling (404s, method not allowed)
  - Edge cases (empty update body, extra fields behavior, bulk create)
- `test_notes.py`: Basic sanity checks for the Notes API

## Test environment and isolation

- `conftest.py` ensures the project root is importable and configures an in-memory SQLite database for the duration of the test session:
  - Sets `DATABASE_URL=sqlite:///:memory:`
  - The app uses `StaticPool` so the in-memory DB persists across connections during tests
- This means each test run starts with a clean database and will not affect your local `app.db` file

## Common issues

- "No module named 'app'"
  - Run pytest from the project root OR keep `tests/conftest.py` present (it adjusts `sys.path`)
- "No tests ran"
  - Ensure you run `python -m pytest` rather than `python pytest`
  - Make sure test files are named like `test_*.py` and functions `test_*`
- Stale local DB data (dev runs)
  - If you ever switch to file-based SQLite during tests, delete `app.db` to start fresh

## Adding new tests

- Create a new file `test_<feature>.py`
- Use `fastapi.testclient.TestClient` against `from app.main import app`
- Prefer small, focused tests avoiding cross-test dependencies
- For request payloads, use helper builders to reduce duplication (see `create_note_payload` in `test_notes_api.py`)

## Useful pytest options

- `-q`: quiet mode
- `-k <expr>`: run tests matching expression
- `-x`: stop on first failure
- `-vv`: verbose output
- `--maxfail=1`: stop after first failure

Examples:
```
python -m pytest -k "create and not invalid" -vv
python -m pytest --maxfail=1 -x
```
