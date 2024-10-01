from fastapi import APIRouter, Depends
from ..schemas import PredictionInput, PredictionOutput
from ..utils import get_model_instance

# Création d'un routeur FastAPI pour les prédictions
router = APIRouter()

# Définition d'une route POST pour les prédictions
@router.post("/predict", response_model=PredictionOutput)
def predict(input: PredictionInput):
    """
    Endpoint pour effectuer une prédiction de classification de texte.

    Cette fonction reçoit un texte en entrée, utilise le modèle ML chargé
    pour faire une prédiction, et retourne le résultat de la classification.

    Args:
        input (PredictionInput): L'objet contenant le texte à classifier.

    Returns:
        PredictionOutput: Un objet contenant la prédiction du modèle.

    Raises:
        HTTPException: En cas d'erreur lors de la prédiction (géré par FastAPI).
    """
    # Obtention d'une instance du modèle
    model = get_model_instance()
    
    # Réalisation de la prédiction en utilisant le texte d'entrée
    # Note: model.predict attend une liste de textes, d'où l'utilisation de [input.text]
    prediction = model.predict([input.text])[0]
    
    # Retour du résultat de la prédiction
    return PredictionOutput(prediction=prediction)