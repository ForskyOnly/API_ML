import mlflow
import os
from dotenv import load_dotenv

load_dotenv()

def get_model():
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")
    run_id = os.getenv("BEST_RUN_ID")
    print(f"MLFLOW_TRACKING_URI: {mlflow_uri}")
    print(f"BEST_RUN_ID: {run_id}")
    
    mlflow.set_tracking_uri(mlflow_uri)
    if run_id is None:
        raise ValueError("BEST_RUN_ID n'est pas défini dans le fichier .env")
    
    try:
        model_path = f"/api_ml/models/mlruns/650145881295194294/{run_id}/artifacts/model"
        print(f"Tentative de chargement du modèle depuis : {model_path}")
        model = mlflow.pyfunc.load_model(model_path)
        print("Modèle chargé avec succès")
        return model
    except Exception as e:
        print(f"Erreur lors du chargement du modèle : {str(e)}")
        raise
    
model = None

def get_model_instance():
    global model
    if model is None:
        model = get_model()
    return model