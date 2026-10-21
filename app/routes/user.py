import sqlite3
import re

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from app.database import iter_connection
from app.security import create_access_token, hash_password, verify_password
from app.responses import api_response


router = APIRouter(prefix="/user", tags=["user"])
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class SignupRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=1, max_length=1024)
    name: str = Field(min_length=1, max_length=100)


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=1, max_length=1024)


@router.post("/signup")
def signup(payload: SignupRequest, connection: sqlite3.Connection = Depends(iter_connection)):
    email = payload.email.strip().lower()
    name = payload.name.strip()
    if not EMAIL_PATTERN.fullmatch(email) or not name:
        return api_response(400, "Invalid email or name")

    try:
        connection.execute(
            "INSERT INTO users (email, password_hash, name) VALUES (?, ?, ?)",
            (email, hash_password(payload.password), name),
        )
        connection.commit()
    except sqlite3.IntegrityError:
        return api_response(status.HTTP_409_CONFLICT, "Email already registered")
    return api_response(status.HTTP_201_CREATED, "Signup successful")


@router.post("/login")
def login(payload: LoginRequest, connection: sqlite3.Connection = Depends(iter_connection)):
    email = payload.email.strip().lower()
    user = connection.execute("SELECT id, email, name, password_hash FROM users WHERE email = ?", (email,)).fetchone()
    if user is None or not verify_password(payload.password, user["password_hash"]):
        return api_response(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")

    token = create_access_token(str(user["id"]))
    return api_response(status.HTTP_200_OK, "Login successful", {"access_token": token, "token_type": "bearer", "user": {"id": user["id"], "email": user["email"], "name": user["name"]}})
