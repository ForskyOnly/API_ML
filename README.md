# 🚀 API de Classification des Données à Risque


## 🎯 À propos du projet

Ce projet est une API de classification des données à risque, utilisant des modèles de machine learning pour prédire le niveau de risque associé à un texte donné.

## ✨ Fonctionnalités

- 🔍 Classification de texte en temps réel
- 🔐 Authentification par clé API
- 📊 Utilisation de modèles MLflow pour les prédictions
- 🐳 Conteneurisation avec Docker pour un déploiement facile

## 🛠 Prérequis

- Python 3.9+
- Docker
- Compte Azure (pour le déploiement)

## 🚀 Installation

1. Clonez le dépôt :
   ```
   git clone https://github.com/votre-username/votre-repo.git
   cd votre-repo
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
   cp .env.example .env
   ```
   Éditez le fichier `.env` avec vos propres valeurs.

## 🖥 Utilisation

Pour lancer l'API localement :

```
uvicorn api.app.main:app --reload
```

L'API sera accessible à l'adresse `http://localhost:8000`.

## 🌐 Déploiement

1. Construisez l'image Docker :
   ```
   docker build -t votre-image:tag .
   ```

2. Poussez l'image vers Azure Container Registry :
   ```
   docker push votre-acr.azurecr.io/votre-image:tag
   ```

3. Déployez sur Azure Container Instances en utilisant le portail Azure ou Azure CLI.

4. Configurez les variables d'environnement dans Azure :
   - API_KEY
   - API_KEY_NAME
   - MLFLOW_TRACKING_URI
   - BEST_RUN_ID

## 🤝 Contribution

Les contributions sont les bienvenues ! Consultez le fichier `CONTRIBUTING.md` pour plus d'informations.

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
