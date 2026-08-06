from typing import TypeVar

from sqlmodel import SQLModel, Session, create_engine

from app.utils import env


engine = create_engine(f"{env.DATABASE_URL}")

def get_session():
    with Session(bind=engine) as session:
        yield session

T = TypeVar("T", bound=SQLModel)
def safe_call(t:T | None, model:str, key:str, value:str) -> T:
    if not t:
        raise ValueError(f"{model} with {key}:{value} is not found.")
    return t