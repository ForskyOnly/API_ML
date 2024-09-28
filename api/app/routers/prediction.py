from fastapi import APIRouter, Depends
from ..schemas import PredictionInput, PredictionOutput
from ..utils import get_model_instance
router = APIRouter()

@router.post("/predict", response_model=PredictionOutput)
def predict(input: PredictionInput):
    model = get_model_instance()
    prediction = model.predict([input.text])[0]
    return PredictionOutput(prediction=prediction)