from sqlmodel import Session

from app.dtos.base import ModificationResult
from app.dtos.inputs import AccountForm


def create(form:AccountForm, session:Session) -> ModificationResult:
    ...

def find_by_id(account_id:int, session:Session):
    ...