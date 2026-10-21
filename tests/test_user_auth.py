import sqlite3

from app.security import decode_access_token


def test_signup_creates_user_and_stores_password_hash(client, monkeypatch, tmp_path):
    database_file = tmp_path / "test_users.sqlite3"
    monkeypatch.setenv("DATABASE_PATH", str(database_file))
    response = client.post(
        "/user/signup", json={"email": "alice@example.com", "password": "secret", "name": "Alice"}
    )

    assert response.status_code == 201
    assert response.json() == {"code": 201, "message": "Signup successful", "result": None}
    with sqlite3.connect(database_file) as connection:
        stored_hash = connection.execute("SELECT password_hash FROM users").fetchone()[0]
    assert stored_hash != "secret"
    assert stored_hash.startswith("pbkdf2_sha256$")


def test_duplicate_signup_returns_409(client):
    body = {"email": "alice@example.com", "password": "secret", "name": "Alice"}
    assert client.post("/user/signup", json=body).status_code == 201

    response = client.post("/user/signup", json=body)

    assert response.status_code == 409
    assert response.json()["code"] == 409
    assert set(response.json()) == {"code", "message", "result"}


def test_signup_email_is_case_insensitive(client):
    assert client.post(
        "/user/signup", json={"email": "Alice@Example.com", "password": "secret", "name": "Alice"}
    ).status_code == 201

    response = client.post(
        "/user/signup", json={"email": "alice@example.com", "password": "secret", "name": "Alice"}
    )

    assert response.status_code == 409


def test_login_returns_valid_jwt(client):
    client.post("/user/signup", json={"email": "alice@example.com", "password": "secret", "name": "Alice"})

    response = client.post("/user/login", json={"email": "alice@example.com", "password": "secret"})

    assert response.status_code == 200
    assert set(response.json()) == {"code", "message", "result"}
    assert response.json()["message"] == "Login successful"
    result = response.json()["result"]
    assert response.json()["code"] == 200
    assert result["token_type"] == "bearer"
    assert decode_access_token(result["access_token"])["sub"] == "1"
    assert result["user"] == {"id": 1, "email": "alice@example.com", "name": "Alice"}


def test_login_with_unknown_email_or_wrong_password_returns_401(client):
    client.post("/user/signup", json={"email": "alice@example.com", "password": "secret", "name": "Alice"})

    for body in (
        {"email": "missing@example.com", "password": "secret"},
        {"email": "alice@example.com", "password": "wrong"},
    ):
        response = client.post("/user/login", json=body)
        assert response.status_code == 401
        assert response.json()["code"] == 401
        assert set(response.json()) == {"code", "message", "result"}


def test_signup_rejects_invalid_email_and_blank_name(client):
    invalid_email = client.post(
        "/user/signup", json={"email": "invalid", "password": "secret", "name": "Alice"}
    )
    blank_name = client.post(
        "/user/signup", json={"email": "alice@example.com", "password": "secret", "name": " "}
    )

    assert invalid_email.status_code == 400
    assert blank_name.status_code == 400


def test_token_signature_is_verified(client):
    client.post("/user/signup", json={"email": "alice@example.com", "password": "secret", "name": "Alice"})
    token = client.post("/user/login", json={"email": "alice@example.com", "password": "secret"}).json()["result"]["access_token"]
    header, payload, signature = token.split(".")
    changed_signature = ("A" if signature[0] != "A" else "B") + signature[1:]

    try:
        decode_access_token(f"{header}.{payload}.{changed_signature}")
    except ValueError:
        pass
    else:
        raise AssertionError("Tampered JWT must be rejected")
