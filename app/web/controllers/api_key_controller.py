from fastapi import APIRouter, Request

from app.web.deps.auth import WebAuthentication
from app.web.deps.template import view


router = APIRouter(prefix="/api-keys")

@router.get("/")
def index(request:Request):
    return view("api-keys/list", request)

@router.get("/create")
def create_view(
    request:Request,
    authentication:WebAuthentication):
    return view("api-keys/create", request, context={"user": authentication.model_dump(exclude=["password"])})