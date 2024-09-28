import mlflow
import os
from dotenv import load_dotenv

load_dotenv()

def get_model():
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    run_id = os.getenv("BEST_RUN_ID")
    return mlflow.pyfunc.load_model(f"runs:/{run_id}/model")

model = None

def get_model_instance():
    global model
    if model is None:
        model = get_model()
    return model