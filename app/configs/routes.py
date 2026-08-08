from fastapi import APIRouter, Depends

from app.api import account_api, api_key_api, auth_api, test_ai_api
from app.deps.auth import require_authentication, require_api_key



annonymous = APIRouter()
authenticated = APIRouter(dependencies=[Depends(require_authentication)])
nlu_router = APIRouter(dependencies=[Depends(require_api_key)])

annonymous.include_router(router=auth_api.router)

authenticated.include_router(router=account_api.router)
authenticated.include_router(router=api_key_api.router)

nlu_router.include_router(router=test_ai_api.router)
from app.api import prediction_api
nlu_router.include_router(router=prediction_api.router)