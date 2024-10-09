


# 🚀 API de Classification des Données à Risque

## 📋 Table des matières
- [À propos du projet](#à-propos-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [ML Ops et Dashboard](#ml-ops-et-dashboard)
- [Déploiement](#déploiement)
- [Contribution](#contribution)
- [Licence](#licence)

## 🎯 À propos du projet

Ce projet est une API de classification des données à risque, utilisant des modèles de machine learning pour prédire le niveau de risque associé à un texte donné.

## ✨ Fonctionnalités

- 🔍 Classification de texte en temps réel
- 🔐 Authentification par clé API
- 📊 Utilisation de modèles MLflow pour les prédictions
- 🐳 Conteneurisation avec Docker pour un déploiement facile
- 📈 Dashboard interactif pour le suivi des performances des modèles

## 🛠 Prérequis

- Python 3.9+
- Docker
- Compte Azure (pour le déploiement)

## 🚀 Installation

1. Clonez le dépôt :
   ```
   git clone https://github.com/ForskyOnly/API_ML/.git
   cd api_ml
   ```

2. Créez un environnement virtuel :
   ```
   python -m venv venv
   source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
   ```

3. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

4. Configurez les variables d'environnement :
   ```
   MLFLOW_TRACKING_URI= chemin vers le dossier mlruns
   BEST_RUN_ID= meilleir run id
   API_KEY= la clef api
   API_KEY_NAME=nom de l'api_key
   ```
   Éditez le fichier `.env` avec vos propres valeurs.

## 🖥 Utilisation

Pour lancer l'API localement :

```
uvicorn api.app.main:app --reload
```

L'API sera accessible à l'adresse `http://localhost:8000`.

## 🛠 ML Ops et Dashboard

### MLflow

MLflow est utilisé pour le suivi des expériences, la gestion des modèles et le déploiement.

Pour accéder à l'interface MLflow, exécutez :

```
mlflow ui
```

### Dashboard de Monitoring

Un dashboard interactif a été développé avec Streamlit pour visualiser les performances des modèles.

Pour lancer le dashboard :

```
streamlit run ml_ops/dashboard.py
```

#### Fonctionnalités principales du dashboard :

1. Sélection du modèle
2. Affichage des meilleurs paramètres
3. Visualisation des métriques (précision, rappel, score F1)
4. Analyse du drift
5. Matrice de confusion
6. Comparaison des modèles
7. Historique des runs

### Intégration Continue / Déploiement Continu (CI/CD)

Nous utilisons GitHub Actions pour automatiser les tests, la construction des images Docker et le déploiement sur Azure.

### Monitoring en Production

- Logs : Utilisation du logging Python standard, capturé et géré par Azure.
- Alertes : Configurées dans Azure pour notifier en cas de problèmes.

## 🌐 Déploiement

### Pipeline CI/CD

Ce projet utilise une pipeline CI/CD configurée avec GitHub Actions. Pour l'utiliser :

1. Configurez les secrets suivants dans les paramètres de votre dépôt GitHub (Settings > Secrets and variables > Actions) :
   - `API_KEY` : Votre clé API secrète
   - `DOCKER_HUB_USERNAME` : Votre nom d'utilisateur Docker Hub
   - `DOCKER_HUB_ACCESS_TOKEN` : Votre token d'accès Docker Hub

2. Poussez vos modifications sur la branche principale pour déclencher automatiquement la pipeline.

### Déploiement sur Azure

Déployez sur Azure Container Instances en utilisant le portail Azure ou Azure CLI comme suit :

   ```
   az container create \
   --resource-group <nom_groupe_ressources> \
   --name <nom_conteneur> \
   --image <nom_utilisateur_dockerhub>/apiml:<tag_image> \
   --ports 80 8000 \
   --dns-name-label <nom_dns_unique> \
   --environment-variables \
   API_KEY_NAME=access_token \
   BEST_RUN_ID=<id_meilleure_execution_mlflow> \
   MLFLOW_TRACKING_URI=file:///api_ml/models/mlruns \
   API_KEY=<votre_cle_api_secrete>
   ```

Remplacez les valeurs entre `<>` par vos propres paramètres.

Assurez-vous d'avoir configuré Azure CLI et d'avoir les permissions nécessaires pour créer des ressources dans votre abonnement Azure.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.


