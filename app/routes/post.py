import sqlite3

from fastapi import APIRouter, Depends, Query
from app.database import iter_connection
from app.responses import api_response


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("")
def list_posts(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    connection: sqlite3.Connection = Depends(iter_connection),
):
    total = connection.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
    offset = (page - 1) * page_size
    rows = connection.execute(
        "SELECT id, title, content, author, created_at FROM posts ORDER BY id DESC LIMIT ? OFFSET ?",
        (page_size, offset),
    ).fetchall()
    return api_response(
        200,
        "Posts retrieved successfully",
        {
                "posts": [dict(row) for row in rows],
                "pagination": {"page": page, "page_size": page_size, "total": total},
        },
    )
