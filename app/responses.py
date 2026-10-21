from typing import Any

from fastapi.responses import JSONResponse


def api_response(status_code: int, message: str, result: Any = None) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"code": status_code, "message": message, "result": result},
    )
