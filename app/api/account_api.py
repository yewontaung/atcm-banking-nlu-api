from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.data.database import get_session
from app.data.enums import AccountRole
from app.data.models import Account
from app.deps.auth import authentication
from app.services import account_service


router = APIRouter(prefix="/accounts")

@router.get("/{account_id}")
def profile_info(account_id:int, authentication:Account = Depends(authentication), session:Session = Depends(get_session)):
    if authentication.account_role != AccountRole.ADMIN and account_id != authentication.account_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail={
                "message": "You cannot access to this endpoint."
            }
        )
    return account_service.find_by_id(account_id, session)