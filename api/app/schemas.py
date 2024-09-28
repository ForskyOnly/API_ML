from pydantic import BaseModel

class PredictionInput(BaseModel):
    text: str

class PredictionOutput(BaseModel):
    prediction: str