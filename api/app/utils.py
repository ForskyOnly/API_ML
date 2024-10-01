import mlflow
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

def get_model():
    """
    Charge le modèle MLflow à partir des chemins spécifiés.

    Cette fonction tente de charger le modèle MLflow en utilisant les informations
    de configuration stockées dans les variables d'environnement. Elle essaie d'abord
    le chemin Docker, puis le chemin local si le premier échoue.

    Returns:
        object: Le modèle MLflow chargé.

    Raises:
        ValueError: Si le BEST_RUN_ID n'est pas défini ou si le modèle ne peut pas être chargé.
    """
    # Récupération des variables d'environnement nécessaires
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI")
    run_id = os.getenv("BEST_RUN_ID")
    print(f"MLFLOW_TRACKING_URI: {mlflow_uri}")
    print(f"BEST_RUN_ID: {run_id}")
    
    # Configuration de l'URI de tracking MLflow
    mlflow.set_tracking_uri(mlflow_uri)
    if run_id is None:
        raise ValueError("BEST_RUN_ID n'est pas défini dans le fichier .env")
    
    # Définition des chemins possibles pour le modèle
    docker_path = f"/api_ml/models/mlruns/650145881295194294/{run_id}/artifacts/model"
    local_path = f"./models/mlruns/650145881295194294/{run_id}/artifacts/model"
    
    # Tentative de chargement du modèle à partir des chemins disponibles
    for path in [docker_path, local_path]:
        try:
            print(f"Tentative de chargement du modèle depuis : {path}")
            model = mlflow.pyfunc.load_model(path)
            print("Modèle chargé avec succès")
            return model
        except Exception as e:
            print(f"Erreur lors du chargement du modèle depuis {path}: {str(e)}")
    
    # Si aucun chemin n'a fonctionné, on lève une exception
    raise ValueError("Impossible de charger le modèle à partir des chemins disponibles")

# Variable globale pour stocker l'instance unique du modèle
model = None

def get_model_instance():
    """
    Récupère ou crée une instance unique du modèle (pattern Singleton).

    Cette fonction vérifie si une instance du modèle existe déjà. Si ce n'est pas le cas,
    elle appelle get_model() pour en créer une. Cela garantit qu'une seule instance
    du modèle est utilisée dans toute l'application, optimisant ainsi l'utilisation
    de la mémoire et les performances.

    Returns:
        object: L'instance unique du modèle MLflow.
    """
    global model
    if model is None:
        model = get_model()
    return model