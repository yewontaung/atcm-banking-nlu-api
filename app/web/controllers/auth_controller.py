from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.data.database import get_session
from app.data.enums import AccountRole
from app.dtos.inputs import AccountForm, SignInForm
from app.services import account_service, auth_service
from app.web.deps.advisor import handle_web_exception
from app.web.deps.template import view


router = APIRouter(prefix="/auth")

@router.get("/sign-up")
def sign_up_view(request:Request):
    return view("auth/sign-up", request)

@router.post("/sign-up")
@handle_web_exception(redirect_url="/web/auth/sign-up")
def sign_up(
    form:Annotated[AccountForm, Form()],
    request:Request, 
    session:Session = Depends(get_session)):
    account_service.create(form, session)
    url = request.url_for("sign_in_view")
    return RedirectResponse(
        url=url, status_code=HTTPStatus.SEE_OTHER
    )

@router.get("/sign-in")
def sign_in_view(request:Request):
    return view("auth/sign-in", request)

@router.post("/sign-in")
@handle_web_exception(redirect_url="/web/auth/sign-in")
def sign_in(
    request:Request,
    form:Annotated[SignInForm, Form()],
    session:Session = Depends(get_session)):

    result = auth_service.sign_in(form, session)

    response = RedirectResponse(
        url=request.url_for("dashboard_page") if result.account_role == AccountRole.ADMIN else "/web/api-keys",
        status_code=HTTPStatus.SEE_OTHER,
    )

    response.set_cookie(
        key="access_token", 
        value=result.access_token, 
        httponly=True,
        secure=False,
        samesite="lax")


    return response

@router.post("/sign-out")
def sign_out():
    response = RedirectResponse(
        url="/web/auth/sign-in",
        status_code=HTTPStatus.SEE_OTHER
    )

    response.delete_cookie("access_token")

    return response