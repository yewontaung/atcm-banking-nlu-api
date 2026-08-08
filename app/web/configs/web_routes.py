from fastapi import APIRouter, Depends, Request

from app.web.controllers import api_key_controller, auth_controller, dashboard_controller, overview_controller
from app.web.deps.auth import require_web_authentication
from app.web.deps.template import view


controller = APIRouter()
annonymous_controller = APIRouter()
authenticated_controller = APIRouter(dependencies=[Depends(require_web_authentication)])

annonymous_controller.include_router(router=auth_controller.router)
authenticated_controller.include_router(router=api_key_controller.router)
authenticated_controller.include_router(router=dashboard_controller.router)
authenticated_controller.include_router(router=overview_controller.router)

controller.include_router(router=annonymous_controller)
controller.include_router(router=authenticated_controller)

@controller.get("/")
def welcome(request:Request):
    return view("index", request)

@controller.get("/forbidden")
def forbidden(request:Request):
    return view("forbidden", request)