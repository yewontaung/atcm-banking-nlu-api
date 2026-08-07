from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.data.database import get_session
from app.deps.auth import Authentication
from app.dtos.inputs import APIKeyForm
from app.dtos.searches import APIKeySearch
from app.services import api_key_service


router = APIRouter(prefix="/api-keys")

@router.post("/")
def generate(
    form:APIKeyForm, 
    authentication:Authentication,
    session:Session = Depends(get_session)):
    return api_key_service.generate_key(form, authentication.account_id, session)

@router.get("/")
def index(
    search:APIKeySearch = Depends(),
    page:int = Query(1),
    size:int = Query(10),
    session:Session = Depends(get_session)
):
    return api_key_service.search(search, page, size, session)