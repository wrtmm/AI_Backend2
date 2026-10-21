import os
import sqlite3
from pathlib import Path
from typing import Iterator

from app.course_catalog import seed_courses


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parent.parent / "users.sqlite3"


def database_path() -> Path:
    return Path(os.getenv("DATABASE_PATH", str(DEFAULT_DATABASE_PATH)))


def get_connection() -> sqlite3.Connection:
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL
            )"""
        )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                subtitle TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                level TEXT NOT NULL,
                price INTEGER NOT NULL CHECK (price >= 0),
                thumbnail_url TEXT NOT NULL,
                instructor TEXT NOT NULL,
                rating REAL NOT NULL CHECK (rating >= 0 AND rating <= 5),
                student_count INTEGER NOT NULL CHECK (student_count >= 0),
                total_lectures INTEGER NOT NULL CHECK (total_lectures >= 0),
                total_duration_minutes INTEGER NOT NULL CHECK (total_duration_minutes >= 0),
                curriculum TEXT NOT NULL
            )"""
        )
        seed_courses(connection)
        connection.execute(
            """CREATE TABLE IF NOT EXISTS payment_orders (
                payment_id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                course_id INTEGER NOT NULL REFERENCES courses(id),
                order_name TEXT NOT NULL,
                amount INTEGER NOT NULL CHECK (amount >= 0),
                currency TEXT NOT NULL DEFAULT 'KRW',
                status TEXT NOT NULL CHECK (status IN ('PENDING', 'PAID')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                paid_at TEXT
            )"""
        )
        connection.execute(
            """CREATE UNIQUE INDEX IF NOT EXISTS one_pending_order_per_user_course
               ON payment_orders(user_id, course_id) WHERE status = 'PENDING'"""
        )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                course_id INTEGER NOT NULL REFERENCES courses(id),
                payment_id TEXT NOT NULL UNIQUE REFERENCES payment_orders(payment_id),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (user_id, course_id)
            )"""
        )


def iter_connection() -> Iterator[sqlite3.Connection]:
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()
