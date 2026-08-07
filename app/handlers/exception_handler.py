from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse


def handle_value_error(_:Request, e:ValueError):
    return JSONResponse(
        content={"message": str(e)},
        status_code=HTTPStatus.BAD_REQUEST,
    )