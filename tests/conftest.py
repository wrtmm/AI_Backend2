import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    database_file = tmp_path / "test_users.sqlite3"
    monkeypatch.setenv("DATABASE_PATH", str(database_file))
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key")

    from main import create_app

    app = create_app()
    with TestClient(app) as test_client:
        yield test_client
