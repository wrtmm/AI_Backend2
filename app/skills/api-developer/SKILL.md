---
name: api-developer
description: Implement FastAPI APIs in this repository's app/ backend and add pytest coverage that verifies the API behavior.
---

# FastAPI API implementation

Use this skill when implementing or changing HTTP APIs in this repository. Inspect the relevant application and test files first, then make the smallest coherent change that fulfills the request, including automated tests.

## Project conventions

- `main.py` creates the FastAPI application with `create_app()`, initializes the database in lifespan, and includes routers. Put endpoints in `app/routes/<domain>.py`; register new routers through `main.py`.
- Keep shared database behavior in `app/database.py` and security helpers in `app/security.py`. Routes use `APIRouter`, `Depends(iter_connection)`, standard-library `sqlite3`, and Pydantic request models. Use parameterized SQL and commit writes.
- Existing endpoints return a JSON envelope shaped as `{"code": <status>, "result": ...}` and declare status codes explicitly. Preserve an existing route's contract when extending it; follow neighboring endpoints for new routes unless the request specifies another contract.
- `tests/conftest.py` provides a `TestClient` fixture with a temporary SQLite file through `DATABASE_PATH` and a test JWT secret. Add or update pytest tests in `tests/` that exercise the API through `TestClient`, including relevant success and failure behavior.

## Implementation and verification

- Define request and response shapes with Pydantic or the established JSON envelope. Validate input at the request boundary and use meaningful HTTP status codes.
- Keep route handlers focused. Put reusable persistence or security logic in the existing backend modules when appropriate; avoid duplicating helpers across routes.
- Keep test database state isolated with the existing fixture or `tmp_path`; never point tests at the default local database.
- Run the relevant tests while iterating, then run the full backend suite with `pytest`. Fix failures caused by the change and report the test result accurately. Do not claim a pass when tests were not run or failed.

## Database path note

Repository-level `AGENTS.md` describes SQLite as `app.db`, while current `app/database.py` defaults to `users.sqlite3`; tests override this using `DATABASE_PATH`. Inspect the active implementation and existing data before changing database-path behavior. For API work, use the existing connection dependency and avoid unrelated database migrations or path changes.
