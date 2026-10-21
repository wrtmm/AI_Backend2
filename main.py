from contextlib import asynccontextmanager
import os

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import initialize_database
from app.routes.user import router as user_router
from app.routes.post import router as post_router
from app.routes.course import router as course_router
from app.routes.payment import router as payment_router
from app.responses import api_response


def _cors_origins() -> list[str]:
    defaults = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    configured = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "").split(",")]
    return list(dict.fromkeys(origin for origin in [*defaults, *configured] if origin and origin != "*"))


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        initialize_database()
        yield

    app = FastAPI(title="AI Backend API", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins(),
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):
        return api_response(422, "Request validation failed", {"errors": exc.errors()})

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_: Request, exc: StarletteHTTPException):
        message = exc.detail if isinstance(exc.detail, str) else "HTTP request failed"
        return api_response(exc.status_code, message)

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(_: Request, __: Exception):
        return api_response(500, "Internal server error")

    app.include_router(user_router)
    app.include_router(post_router)
    app.include_router(course_router)
    app.include_router(payment_router)
    return app


app = create_app()
