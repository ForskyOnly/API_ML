from fastapi.testclient import TestClient
from app.main import app
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()
API_KEY = os.getenv("API_KEY")


client = TestClient(app)

def test_predict():
    """
    Teste le fonctionnement normal de l'endpoint de prédiction.
    Vérifie que la requête avec une clé API valide retourne un statut 200
    et contient une prédiction dans la réponse.
    """
    response = client.post("/predict", 
                           json={"text": "Exemple de texte à classifier"},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_predict_unauthorized():
    """
    Teste le comportement de l'API lorsqu'une clé API invalide est utilisée.
    Vérifie que la requête est rejetée avec un statut 403 (Forbidden).
    """
    response = client.post("/predict", 
                           json={"text": "Exemple de texte à classifier"},
                           headers={"access_token": "mauvaise_cle"})
    assert response.status_code == 403
    
def test_predict_dcp2():
    """
    Teste la prédiction pour un exemple de texte de catégorie DCP2.
    Vérifie que la prédiction retournée est correcte.
    """
    response = client.post("/predict", 
                           json={"text": "LIEU_NAISSANCE;Ville de naissance de la personne."},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert response.json()["prediction"] == "DCP2"

def test_predict_dcp3():
    """
    Teste la prédiction pour un exemple de texte de catégorie DCP3.
    Vérifie que la prédiction retournée est correcte.
    """
    response = client.post("/predict", 
                           json={"text": "MT_SALAIRE_NET;Salaire net mensuel de la personne"},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert response.json()["prediction"] == "DCP3"

def test_predict_dco3():
    """
    Teste la prédiction pour un exemple de texte de catégorie DCO3.
    Vérifie que la prédiction retournée est correcte.
    """
    response = client.post("/predict", 
                           json={"text": "OBJECTIFS_VENTES;Objectifs de vente mensuels ou annuels du vendeur"},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert response.json()["prediction"] == "DCO3"
        
def test_predict_nodcp():
    """
    Teste la prédiction pour un exemple de texte de catégorie NONDCP.
    Vérifie que la prédiction retournée est correcte.
    """
    response = client.post("/predict", 
                           json={"text": "DATE_DEBUT; début du projet.;NONDCP"},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert response.json()["prediction"] == "NONDCP"
    
def test_predict_dcm1():
    """
    Teste la prédiction pour un exemple de texte de catégorie DCM1.
    Vérifie que la prédiction retournée est correcte.
    """
    response = client.post("/predict", 
                           json={"text": "BILAN_PATRIMONIAL;Valeur globale des actifs et passifs de l'entreprise."},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert response.json()["prediction"] == "DCM1"
