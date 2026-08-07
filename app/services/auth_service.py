from sqlmodel import Session, select

from app.data.database import safe_call
from app.data.models import Account
from app.deps import auth
from app.dtos.inputs import SignInForm
from app.dtos.outputs import AuthResult
from app.utils.auth_token import encode_token
from app.utils.hashing import verify_password


def sign_in(form:SignInForm, session:Session) -> AuthResult:
    account = safe_call(session.exec(
        select(Account).where(Account.account_email == form.email)
    ).first(), "Account", "email", form.email)

    if not verify_password(form.password, account.hashed_password):
        raise ValueError(f"Wrong password.")
    token = encode_token({
        "account_id": account.account_id,
        "account_email": account.account_email,
        "full_name": account.full_name,
        "account_role": account.account_role,
    })

    return AuthResult(
        account_id=account.account_id,
        access_token=token
    )
