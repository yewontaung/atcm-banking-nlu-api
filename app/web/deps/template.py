from typing import Any
from zoneinfo import ZoneInfo

from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(
    directory="./templates"
)

def format_datetime(value, format="%b %d, %Y at %I:%M %p", target_tz="Asia/Yangon"):
    if value is None:
        return ""
    if value.tzinfo is None:
        value = value.replace(tzinfo=ZoneInfo("UTC"))
    return value.astimezone(ZoneInfo(target_tz)).strftime(format)

# Add filter to Jinja environment
templates.env.filters["format_datetime"] = format_datetime

def view(path:str, request:Request, context:dict[str, Any] = {}, suffix:str = "html"):
    return templates.TemplateResponse(
        request=request,
        name=f"{path}.{suffix}",
        context=context,
    )