from fastapi import APIRouter, Request

from app.web.deps.template import view


router = APIRouter(prefix="/admin/dashboard")

@router.get("/")
def dashboard_page(request:Request):
    return view("admin/dashboard", request, context={
        "user": {
            "full_name": "Ye Wont Aung",
            "account_id": "1",
        },
        "stats": "something"
    },)