from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.data.database import get_session
from app.data.enums import AccountRole
from app.services import account_service, api_key_service, dashboard_service
from app.web.deps.auth import WebAuthentication
from app.web.deps.template import view


router = APIRouter(prefix="/admin/dashboard")

@router.get("/")
def dashboard_page(request:Request, authentication:WebAuthentication, session:Session = Depends(get_session)):
    if authentication.account_role != AccountRole.ADMIN:
        return RedirectResponse(
            url="/web/forbidden",
            status_code=HTTPStatus.SEE_OTHER,
        )
    context = {
        "user": authentication.model_dump(exclude=["password"]),
    }

    users = account_service.find_all(session)
    context["users"] = users

    keys = api_key_service.find_all(session)
    context["keys"] = keys

    stats = dashboard_service.get_stats(session)
    context["stats"] = stats

    return view("admin/dashboard", request, context)