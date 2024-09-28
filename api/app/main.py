from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from .utils import get_model
from .routers import prediction
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Depends(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Logique de démarrage
    get_model()
    yield
    # Logique de fermeture (si nécessaire)

app = FastAPI(lifespan=lifespan)

app.include_router(prediction.router, dependencies=[Depends(get_api_key)])

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de classification des données à Risque"}