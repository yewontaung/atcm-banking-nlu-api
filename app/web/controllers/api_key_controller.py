from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.data.database import get_session
from app.dtos.inputs import APIKeyForm
from app.services import api_key_service
from app.utils.api_key_cache import API_KEY_CACHE
from app.web.deps.advisor import hanle_web_exception
from app.web.deps.auth import WebAuthentication
from app.web.deps.template import view


router = APIRouter(prefix="/api-keys")

@router.get("/")
def index(request:Request, authentication:WebAuthentication, session:Session = Depends(get_session)):
    context = {
        "user": authentication.model_dump(exclude=["password"])
    }

    keys = api_key_service.find_all_by_account_id(authentication.account_id, session)
    context["keys"] = keys

    return view("api-keys/list", request, context)

@router.get("/create")
def create_view(
    request:Request,
    authentication:WebAuthentication,
    key_id:Optional[int] = Query(None),):

    context={"user": authentication.model_dump(exclude=["password"])}

    if key_id:
        result = API_KEY_CACHE.pop(key_id)
        if result:
            project_name, token = result
            context["newKey"] = token
            context["newProjectName"] = project_name

    return view("api-keys/create", request, context)

@router.post("/create")
@hanle_web_exception(redirect_url="/web/api-keys/create")
def create(form:Annotated[APIKeyForm, Form()], request:Request, auth:WebAuthentication, session:Session = Depends(get_session)):
    api_key = api_key_service.generate_key(form, auth.account_id, session, use_cache=True)
    return RedirectResponse(
        url=f"/web/api-keys/create?key_id={api_key.key_id}",
        status_code=HTTPStatus.SEE_OTHER,
    )
