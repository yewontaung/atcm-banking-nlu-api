from fastapi import APIRouter

from app.dtos.inputs import APIKeyForm
from app.services import api_key_service


router = APIRouter(prefix="/api-keys")

@router.post("/")
def generate(form:APIKeyForm):
    return api_key_service.generate_key(form)