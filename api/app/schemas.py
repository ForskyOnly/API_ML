from pydantic import BaseModel

# Définition du modèle d'entrée pour la prédiction
class PredictionInput(BaseModel):
    text: str

# Définition du modèle de sortie pour la prédiction
class PredictionOutput(BaseModel):
    prediction: str