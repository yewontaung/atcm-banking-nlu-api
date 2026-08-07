from typing import TypeVar

from sqlmodel import SQLModel, Session, create_engine, func, select

from app.utils import env
from app.data.models import *
from app.utils.hashing import hash_password

engine = create_engine(f"{env.DATABASE_URL}", echo=env.SHOW_SQL)

def get_session():
    with Session(bind=engine) as session:
        yield session

T = TypeVar("T", bound=SQLModel)
def safe_call(t:T | None, model:str, key:str, value:str) -> T:
    if not t:
        raise ValueError(f"{model} with {key}: {value} is not found.")
    return t

def create_tables():
    SQLModel.metadata.create_all(bind=engine)

def create_admin():
    with Session(engine) as session:
        count = session.exec(select(func.count(Account.account_id))).one_or_none() or 0
        if count == 0:
            account = Account(
                full_name=env.ADMIN_NAME,
                account_email=env.ADMIN_EMAIL,
                hashed_password=hash_password(env.ADMIN_PASSWORD),
                account_role=AccountRole.ADMIN,
            )
            session.add(account)
            session.commit()