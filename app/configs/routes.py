from fastapi import APIRouter

from app.api import prediction_api


annonymous = APIRouter()
authenticated = APIRouter()

authenticated.include_router(router=prediction_api.router)