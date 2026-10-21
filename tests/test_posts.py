from app.database import get_connection


def test_list_posts_returns_empty_list_and_pagination(client):
    response = client.get("/posts")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "message": "Posts retrieved successfully",
        "result": {
            "posts": [],
            "pagination": {"page": 1, "page_size": 20, "total": 0},
        },
    }


def test_list_posts_returns_newest_first_and_supports_pagination(client):
    with get_connection() as connection:
        connection.executemany(
            "INSERT INTO posts (title, content, author) VALUES (?, ?, ?)",
            [(f"title {i}", f"content {i}", "writer") for i in range(1, 4)],
        )

    response = client.get("/posts?page=2&page_size=2")

    assert response.status_code == 200
    result = response.json()["result"]
    assert [post["title"] for post in result["posts"]] == ["title 1"]
    assert result["pagination"] == {"page": 2, "page_size": 2, "total": 3}


def test_list_posts_rejects_invalid_pagination(client):
    response = client.get("/posts?page=0")
    assert response.status_code == 422
    assert set(response.json()) == {"code", "message", "result"}
    assert response.json()["message"] == "Request validation failed"

    too_large = client.get("/posts?page_size=101")
    assert too_large.status_code == 422
    assert set(too_large.json()) == {"code", "message", "result"}


def test_not_found_response_uses_standard_envelope(client):
    response = client.get("/missing")

    assert response.status_code == 404
    assert set(response.json()) == {"code", "message", "result"}
