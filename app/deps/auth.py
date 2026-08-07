from http import HTTPStatus
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from app.data.database import get_session, safe_call
from app.data.enums import APIKeyStatus
from app.data.models import APIKey, Account
from app.utils.auth_token import decode_token
from app.utils.hashing import hash_api_key


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/access-token")
api_key_schema = OAuth2PasswordBearer(tokenUrl="/api-key-token")

def require_authentication(request:Request, token:str = Depends(oauth2_schema), session:Session = Depends(get_session)):
    payload = decode_token(token)
    account = safe_call(session.get(Account, payload.get("account_id")), "Account", "account_id", payload.get("account_id"))
    if payload.get("account_email") != account.account_email or payload.get("account_role") != account.account_role:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid token."
        )
    request.state.authentication = account
    return account

def authentication(request:Request) -> Account:
    if not hasattr(request.state, "authentication"):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Request is not authenticated."
        )
    return request.state.authentication

Authentication = Annotated[Account, Depends(authentication)]

def require_api_key(request:Request, token:str = Depends(api_key_schema), session:Session = Depends(get_session)):
    hashed = hash_api_key(token)
    api_key = safe_call(session.exec(
        select(APIKey).where(APIKey.hashed_api_token == hashed)
    ).first(), "APIKey", "api_key", token)

    if api_key.status != APIKeyStatus.ACTIVE:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=f"You cannot use {api_key.status} key."
        )

    request.state.api_authentication = api_key
    
    return api_key

def api_key_authentication(request:Request) -> APIKey:
    if not hasattr(request.state, "api_authentication"):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Request is not authenticated."
        )
    return request.state.api_authentication

APIAuthentication = Annotated[APIKey, Depends(api_key_authentication)]
