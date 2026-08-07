from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.data.database import get_session
from app.dtos.inputs import AccountForm, SignInForm
from app.services import account_service, auth_service


router = APIRouter(prefix="/auth")

@router.post("/sign-up")
def sign_up(form:AccountForm, session:Session = Depends(get_session)):
    return account_service.create(form, session)

@router.post("/token")
def token(form:SignInForm, session:Session = Depends(get_session)):
    return auth_service.sign_in(form, session)