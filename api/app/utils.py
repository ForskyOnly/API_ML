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
    
    # Chemin pour le déploiement Docker
    docker_path = f"/api_ml/models/mlruns/650145881295194294/{run_id}/artifacts/model"
    # Chemin pour l'exécution locale
    local_path = f"./models/mlruns/650145881295194294/{run_id}/artifacts/model"
    
    for path in [docker_path, local_path]:
        try:
            print(f"Tentative de chargement du modèle depuis : {path}")
            model = mlflow.pyfunc.load_model(path)
            print("Modèle chargé avec succès")
            return model
        except Exception as e:
            print(f"Erreur lors du chargement du modèle depuis {path}: {str(e)}")
    
    raise ValueError("Impossible de charger le modèle à partir des chemins disponibles")

model = None

def get_model_instance():
    global model
    if model is None:
        model = get_model()
    return model