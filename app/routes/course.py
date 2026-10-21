import json
import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database import iter_connection
from app.responses import api_response


router = APIRouter(prefix="/courses", tags=["courses"])

COURSE_FIELDS = (
    "id, title, subtitle, description, category, level, price, thumbnail_url, "
    "instructor, rating, student_count, total_lectures, total_duration_minutes"
)


@router.get("")
def list_courses(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    category: str | None = Query(default=None, min_length=1, max_length=100),
    level: str | None = Query(default=None, min_length=1, max_length=50),
    connection: sqlite3.Connection = Depends(iter_connection),
):
    filters = []
    parameters: list[str | int] = []
    if category is not None:
        filters.append("category = ? COLLATE NOCASE")
        parameters.append(category.strip())
    if level is not None:
        filters.append("level = ? COLLATE NOCASE")
        parameters.append(level.strip())

    where_clause = f" WHERE {' AND '.join(filters)}" if filters else ""
    total = connection.execute(
        f"SELECT COUNT(*) FROM courses{where_clause}", parameters
    ).fetchone()[0]
    offset = (page - 1) * page_size
    rows = connection.execute(
        f"SELECT {COURSE_FIELDS} FROM courses{where_clause} ORDER BY id LIMIT ? OFFSET ?",
        [*parameters, page_size, offset],
    ).fetchall()

    return api_response(
        status.HTTP_200_OK,
        "Courses retrieved successfully",
        {
            "courses": [dict(row) for row in rows],
            "pagination": {"page": page, "page_size": page_size, "total": total},
        },
    )


@router.get("/{course_id}")
def get_course(
    course_id: int,
    connection: sqlite3.Connection = Depends(iter_connection),
):
    row = connection.execute(
        f"SELECT {COURSE_FIELDS}, curriculum FROM courses WHERE id = ?",
        (course_id,),
    ).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    course = dict(row)
    course["curriculum"] = json.loads(course["curriculum"])
    return api_response(
        status.HTTP_200_OK,
        "Course retrieved successfully",
        {"course": course},
    )
