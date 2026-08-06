from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.utils import env


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("========== Launching ATCM Banking API ==========")
    from app.configs import nlu_model
    nlu_model.load_nlu(
        model_name="xlm-roberta-base",
        saved_model_path="./_model/banking_nlu_model_02_d1014_e30.pt",
        intent_metadata_path="./_metadata/intents.json",
        entity_metadata_path="./_metadata/entities.json",
    )
    yield
    print("========== Shutting Down the ATCM Banking API ==========")

app = FastAPI(lifespan=lifespan)

from app.configs import routes

app.include_router(prefix=f"{env.API_VERSION}", router=routes.annonymous)
app.include_router(prefix=f"{env.API_VERSION}", router=routes.authenticated)