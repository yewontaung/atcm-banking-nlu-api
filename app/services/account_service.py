from sqlmodel import Session, desc, select

from app.data.database import safe_call
from app.data.models import Account
from app.dtos.base import ModificationResult
from app.dtos.inputs import AccountForm
from app.dtos.outputs import AccountProfile
from app.utils.hashing import hash_password


def create(form:AccountForm, session:Session) -> ModificationResult:
    if session.exec(select(Account).where(Account.account_email == form.email)).first():
        raise ValueError(f"Account with email: {form.email} exists.")
    if not form.valid:
        raise ValueError(f"Passwords are not same.")
    account = Account(
        full_name=form.full_name,
        account_email=form.email,
        hashed_password=hash_password(form.password),
    )

    session.add(account)
    session.commit()
    session.refresh(account)

    return ModificationResult(result_item=account.account_id, success=True, message="Account created successfully.")

def find_by_id(account_id:int, session:Session) -> AccountProfile:
    account = safe_call(session.get(Account, account_id), "Account", "account_id", account_id)
    return AccountProfile.from_(account)

def find_all(session:Session) -> list[AccountProfile]:
    result = session.exec(
        select(Account).order_by(desc(Account.created_at))
    ).all()
    return [AccountProfile.from_(item) for item in result]