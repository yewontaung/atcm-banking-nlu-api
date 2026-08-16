from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.data import database
from app.handlers.exception_handler import handle_value_error
from app.utils import env
from app.utils.exceptions import WebAuthException
from app.web.configs import web_routes
from app.web.handlers.exception_handler import handle_web_auth_exception


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("========== Launching ATCM Banking API ==========")
    from app.configs import nlu_model
    nlu_model.load_nlu(
        model_name="xlm-roberta-base",
        saved_model_path=env.MODEL_PATH,
        intent_metadata_path="./_metadata/intents.json",
        entity_metadata_path="./_metadata/entities.json",
    )
    database.create_tables()
    database.create_admin()
    yield
    print("========== Shutting Down the ATCM Banking API ==========")

app = FastAPI(lifespan=lifespan)

from app.configs import routes

app.include_router(prefix=f"/api/v{env.API_VERSION}", router=routes.annonymous)
app.include_router(prefix=f"/api/v{env.API_VERSION}", router=routes.authenticated)
app.include_router(prefix=f"/api/v{env.API_VERSION}", router=routes.nlu_router)

app.add_exception_handler(ValueError, handle_value_error)

# web config
app.mount(
    "/static",
    StaticFiles(directory="./static"),
    name="static"
)

app.include_router(prefix=f"/web", router=web_routes.controller, tags=["web"])
app.add_exception_handler(WebAuthException, handle_web_auth_exception)