import json

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.exception.exception import (
    DBTransactionError
)
from src.utils.route_utils import error_loc


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom exception handler for validation errors.
    This handler will be called when a RequestValidationError is raised.
    """
    content = {
        "code": "400 Bad Request",
        "message": "Request is not valid. Please check request body.",
    }
    try:
        errors = json.loads(exc.json())
        content["errors"] = [
            {"field": error_loc(error["loc"]), "message": error["msg"]}
            for error in errors
        ]
    except Exception:  # noqa
        content["description"] = "Request body parsing error."
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=content,
    )



async def database_transaction_exception_handler(
    request: Request, exc: DBTransactionError
):
    return JSONResponse(
        content={
            "code": exc.code,
            "message": exc.message,
        }
    )