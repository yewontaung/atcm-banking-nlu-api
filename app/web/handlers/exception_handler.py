from http import HTTPStatus

from fastapi import Request
from fastapi.responses import RedirectResponse

from app.utils.exceptions import WebAuthException


def handle_web_auth_exception(request:Request, e:WebAuthException):
    return RedirectResponse(url="/web/auth/sign-in", status_code=HTTPStatus.SEE_OTHER)