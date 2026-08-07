from typing import Any

from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(
    directory="./templates"
)

def view(path:str, request:Request, context:dict[str, Any] = {}, suffix:str = "html"):
    return templates.TemplateResponse(
        request=request,
        name=f"{path}.{suffix}",
        context=context,
    )