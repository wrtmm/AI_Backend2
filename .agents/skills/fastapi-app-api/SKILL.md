---
name: fastapi-app-api
description: Implement or change HTTP APIs in this repository's FastAPI backend under app/, following its router, SQLite, validation, response, and pytest conventions.
---

# FastAPI backend API work

Use this skill for backend endpoint work in this repository. First inspect the relevant files and existing route/tests; extend the established design and keep changes within the requested API scope.

## Project conventions

- `main.py` creates the FastAPI application with `create_app()`, initializes the database in lifespan, and includes routers. Put endpoints in `app/routes/<domain>.py`; expose a new router through `main.py`.
- Keep shared database behavior in `app/database.py` and security helpers in `app/security.py`. Routes currently use `APIRouter`, `Depends(iter_connection)`, standard-library `sqlite3`, and Pydantic request models. Use parameterized SQL and commit writes.
- Existing endpoints return a JSON envelope shaped as `{"code": <status>, "result": ...}` and declare status codes explicitly. Preserve a route's existing contract when extending it; follow neighboring endpoints for new routes unless the request specifies another contract.
- `tests/conftest.py` provides a `TestClient` fixture with a temporary SQLite file through `DATABASE_PATH` and a test JWT secret. Add or update pytest tests in `tests/` for behavior and error cases when changing an API.
- Run the relevant pytest tests and, for completion, the full backend suite (`pytest`). Do not claim success if tests were not run or failed.

## Database path note

Repository-level `AGENTS.md` describes SQLite as `app.db`, while current `app/database.py` defaults to `users.sqlite3`; tests override this using `DATABASE_PATH`. Inspect the active implementation and existing data before changing database-path behavior. For API changes, use the existing connection dependency and avoid unrelated database migrations or path changes.

## Implementation guidance

- Define request and response shapes with Pydantic or the established JSON envelope. Validate input at the request boundary and preserve meaningful HTTP status codes.
- Keep route handlers focused. Put reusable persistence or security logic in the existing backend modules when appropriate; do not duplicate helpers across routes.
- Register each new router in `main.py`, then exercise the API through `TestClient` so routing, dependency injection, lifespan initialization, status codes, and response bodies are covered.
- Keep test database state isolated with the existing fixture or `tmp_path`; never point tests at the default local database.
