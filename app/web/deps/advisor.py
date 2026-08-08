from functools import wraps
from http import HTTPStatus
import inspect
from typing import Any, Callable

from fastapi.responses import RedirectResponse


def hanle_web_exception(redirect_url:str) -> Callable:

    def wrapper(func:Callable[..., Any]):

        @wraps(func)
        async def decorate(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if inspect.isawaitable(result):
                    return await result
                return result
            except Exception as e:
                return RedirectResponse(
                    status_code=HTTPStatus.SEE_OTHER,
                    url=f"{redirect_url}?error={str(e)}"
                )
        return decorate

    return wrapper