from fastapi import APIRouter, Request

from app.web.deps.auth import WebAuthentication
from app.web.deps.template import view


router = APIRouter(prefix="/overview")

@router.get("/")
def index(request:Request, auth:WebAuthentication):
    return view("index", request, {
        "user": auth.model_dump(exclude=["password"])
    })