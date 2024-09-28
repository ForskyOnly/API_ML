from fastapi.testclient import TestClient
from app.main import app
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

client = TestClient(app)

def test_predict():
    response = client.post("/predict", 
                           json={"text": "Exemple de texte à classifier"},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert "prediction" in response.json()

def test_predict_unauthorized():
    response = client.post("/predict", 
                           json={"text": "Exemple de texte à classifier"},
                           headers={"access_token": "mauvaise_cle"})
    assert response.status_code == 403
    
def test_predict_dcp2():
    response = client.post("/predict", 
                           json={"text": "LIEU_NAISSANCE;Ville de naissance de la personne."},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert response.json()["prediction"] == "DCP2"

def test_predict_dcp3():
    response = client.post("/predict", 
                           json={"text": "MT_SALAIRE_NET;Salaire net mensuel de la personne"},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert response.json()["prediction"] == "DCP3"


def test_predict_dco3():
    response = client.post("/predict", 
                           json={"text": "OBJECTIFS_VENTES;Objectifs de vente mensuels ou annuels du vendeur"},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert response.json()["prediction"] == "DCO3"
        
    
def test_predict_nodcp():
    response = client.post("/predict", 
                           json={"text": "DATE_DEBUT; début du projet.;NONDCP"},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert response.json()["prediction"] == "NONDCP"
    
    
    
def test_predict_dcm1():
    response = client.post("/predict", 
                           json={"text": "BILAN_PATRIMONIAL;Valeur globale des actifs et passifs de l'entreprise."},
                           headers={"access_token": API_KEY})
    assert response.status_code == 200
    assert response.json()["prediction"] == "DCM1"
    