import secrets

from sqlmodel import Session, exists, func, select
from sqlalchemy.orm import selectinload

from app.data.database import safe_call
from app.data.models import APIKey, Account
from app.dtos.base import PageResult
from app.dtos.inputs import APIKeyForm
from app.dtos.outputs import APIKeyListItem, APIKeyResult
from app.dtos.searches import APIKeySearch
from app.utils.hashing import hash_api_key


def generate_key(form:APIKeyForm, account_id:int, session:Session) -> APIKeyResult:
    if form.user_id != account_id:
        raise ValueError(f"Invalid request for api key.")
    account = safe_call(session.get(Account, account_id), "Account", "account_id", account_id)
    CHECK_PROJECT_NAME = select(
        exists().where(APIKey.project_name == form.project_name, APIKey.created_by == account_id))
    if session.exec(CHECK_PROJECT_NAME).one():
        raise ValueError(f"Project: {form.project_name} exists.")

    api_token = f"ATCM_NLU_{secrets.token_urlsafe(32)}"

    api_key = APIKey(
        project_name=form.project_name,
        hashed_api_token=hash_api_key(api_token),
        created_by=account.account_id,
    )

    session.add(api_key)
    session.commit()
    session.refresh(api_key)

    return APIKeyResult(
        key_id=api_key.key_id,
        project_name=api_key.project_name,
        api_key=api_token,
        message="Please copy and save the api key. You will only this once.",
        creator_id=account.account_id,
        creator_name=account.full_name,
        status=api_key.status,
        created_at=api_key.created_at,
    )

def search(search:APIKeySearch, page:int, size:int, session:Session) -> PageResult[APIKeyListItem]:
    QUERY = select(APIKey).options(
        selectinload(APIKey.creator),
        selectinload(APIKey.updator)
    ).limit(size).offset(size * (page - 1))

    TOTAL = select(func.count(APIKey.key_id))

    result = session.exec(QUERY).all()
    items = [APIKeyListItem.from_(item) for item in result]

    total = session.exec(TOTAL).one_or_none() or 0

    return PageResult(
        items=[items],
        page=page,
        size=size,
        total=total,
    )