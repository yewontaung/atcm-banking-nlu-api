from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from app.data.database import get_session, safe_call
from app.data.models import Account
from app.utils.auth_token import decode_token
from app.utils.exceptions import WebAuthException
from app.web.deps.advisor import handle_web_exception


@handle_web_exception("/web/auth/sign-in")
def require_web_authentication(request:Request, session:Session = Depends(get_session)):
    token = request.cookies.get("access_token")
    if not token:
        raise WebAuthException("Unauthenticated.")
    payload = decode_token(token)
    account = safe_call(session.get(Account, payload.get("account_id")), "Account", "account_id", payload.get("account_id"))
    if payload.get("account_email") != account.account_email or payload.get("account_role") != account.account_role:
        raise WebAuthException("Invalid authentication.")
    request.state.authentication = account
    return account

def web_authentication(request:Request) -> Account:
    if not hasattr(request.state, "authentication"):
        raise WebAuthException("Request is not autheticated.")
    return request.state.authentication

WebAuthentication = Annotated[Account, Depends(web_authentication)]
