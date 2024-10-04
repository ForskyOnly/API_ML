from fastapi import FastAPI, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from .utils import get_model
from .routers import prediction
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Chargement des variables d'environnement
load_dotenv()

# Récupération des variables d'environnement pour l'API key
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME", "access_token")

# Configuration de l'en-tête pour l'API key
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Fonction pour vérifier l'API key
async def get_api_key(api_key_header: str = Depends(api_key_header)):
    """
    Vérifie la validité de la clé API fournie dans l'en-tête de la requête.

    Args:
        api_key_header (str): La clé API fournie dans l'en-tête de la requête.

    Returns:
        str: La clé API si elle est valide.

    Raises:
        HTTPException: Si la clé API est invalide ou manquante.
    """
    if api_key_header == API_KEY:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Clé API invalide"
        )

# Gestionnaire de contexte asynchrone pour le cycle de vie de l'application
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gère le cycle de vie de l'application FastAPI.
    Charge le modèle au démarrage de l'application.

    Args:
        app (FastAPI): L'instance de l'application FastAPI.

    Yields:
        None
    """
    # Logique de démarrage : chargement du modèle
    get_model()
    yield
    # Logique de fermeture (si nécessaire)

# Création de l'application FastAPI
app = FastAPI(lifespan=lifespan)

# Inclusion du routeur de prédiction avec dépendance sur l'API key
app.include_router(prediction.router, dependencies=[Depends(get_api_key)])

# Route racine de l'API
@app.get("/")
def read_root():
    """
    Route racine de l'API.
    Fournit un message de bienvenue simple.

    Returns:
        dict: Un dictionnaire contenant un message de bienvenue.
    """
    return {"message": "Bienvenue sur l'API de classification des données à Risque"}