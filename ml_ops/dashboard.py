import streamlit as st
import mlflow
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from mlflow.tracking import MlflowClient

####################   Ce script crée un tableau de bord Streamlit pour visualiser et analyser les performances  #####################
####################   des modèles de classification entraînés avec MLflow.  ################################################



# Configuration de MLflow
mlflow.set_tracking_uri("file:./mlruns")
client = MlflowClient()

def load_mlflow_data():
    """
    Charge les données des expériences MLflow pour la classification de texte.
    
    Returns:
        DataFrame: Un DataFrame contenant les informations sur les runs MLflow.
    """
    experiment = mlflow.get_experiment_by_name("Classification de texte")
    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])
    return runs

def calculate_drift(train_metric, test_metric):
    """
    Calcule le drift entre les métriques d'entraînement et de test.
    
    Args:
        train_metric (float): Valeur de la métrique pour l'ensemble d'entraînement.
        test_metric (float): Valeur de la métrique pour l'ensemble de test.
    
    Returns:
        float: Le pourcentage de drift calculé.
    """
    return abs(train_metric - test_metric) / train_metric * 100

# Titre du dashboard
st.title("Dashboard des Modèles de Classification de Texte")

# Chargement des données
runs = load_mlflow_data()

# Sélection du modèle
models = runs["params.model"].unique()
selected_model = st.selectbox("Sélectionnez un modèle", models)

# Filtrage des runs pour le modèle sélectionné
model_runs = runs[runs["params.model"] == selected_model]

# Affichage des meilleurs paramètres
st.subheader(f"Meilleurs paramètres pour {selected_model}")
best_run = model_runs.loc[model_runs["metrics.test_accuracy"].idxmax()]
best_params = {k: v for k, v in best_run.items() if k.startswith("params.") and k != "params.model"}
st.json(best_params)

# Affichage des métriques du meilleur run
st.subheader("Métriques du meilleur run")
metrics = ["accuracy", "precision", "recall", "f1"]
col1, col2 = st.columns(2)
for i, metric in enumerate(metrics):
    train_metric = best_run[f"metrics.train_{metric}"]
    test_metric = best_run[f"metrics.test_{metric}"]
    drift = calculate_drift(train_metric, test_metric)
    if i % 2 == 0:
        col1.metric(f"{metric.capitalize()}", f"{test_metric:.4f}", f"Drift: {drift:.2f}%")
    else:
        col2.metric(f"{metric.capitalize()}", f"{test_metric:.4f}", f"Drift: {drift:.2f}%")

# Graphique de comparaison Train vs Test
st.subheader("Comparaison Train vs Test")
fig = go.Figure()
for metric in metrics:
    fig.add_trace(go.Bar(name=f'Train {metric}', x=[metric], y=[best_run[f"metrics.train_{metric}"]], marker_color='blue'))
    fig.add_trace(go.Bar(name=f'Test {metric}', x=[metric], y=[best_run[f"metrics.test_{metric}"]], marker_color='red'))
fig.update_layout(barmode='group', title=f"Métriques Train vs Test pour {selected_model}")
st.plotly_chart(fig)

# Graphique du drift
st.subheader("Drift des Métriques")
drift_data = []
for metric in metrics:
    train_metric = best_run[f"metrics.train_{metric}"]
    test_metric = best_run[f"metrics.test_{metric}"]
    drift = calculate_drift(train_metric, test_metric)
    drift_data.append({"Metric": metric, "Drift (%)": drift})

drift_df = pd.DataFrame(drift_data)
fig = px.bar(drift_df, x="Metric", y="Drift (%)", title=f"Drift des métriques pour {selected_model}")
st.plotly_chart(fig)

# Matrice de confusion
st.subheader("Matrice de Confusion")
run_id = best_run["run_id"]
artifact_uri = client.get_run(run_id).info.artifact_uri
confusion_matrix = mlflow.artifacts.load_dict(f"{artifact_uri}/confusion_matrix.json")
fig = px.imshow(pd.DataFrame(confusion_matrix),
                labels=dict(x="Prédiction", y="Réalité", color="Nombre"),
                x=list(confusion_matrix.keys()),
                y=list(confusion_matrix.keys()),
                title=f"Matrice de Confusion pour {selected_model}")
st.plotly_chart(fig)

# Comparaison des modèles
st.subheader("Comparaison des Modèles")
model_comparison = runs.groupby("params.model")["metrics.test_accuracy"].max().reset_index()
fig = px.bar(model_comparison, x="params.model", y="metrics.test_accuracy", 
             title="Précision des différents modèles", labels={"metrics.test_accuracy": "Précision"})
st.plotly_chart(fig)

# Historique des runs
st.subheader("Historique des Runs")
run_history = runs[["start_time", "params.model", "metrics.test_accuracy"]]
run_history["start_time"] = pd.to_datetime(run_history["start_time"])
fig = px.scatter(run_history, x="start_time", y="metrics.test_accuracy", color="params.model",
                 title="Évolution de la précision au fil du temps", labels={"metrics.test_accuracy": "Précision"})
st.plotly_chart(fig)