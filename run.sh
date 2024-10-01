#!/bin/bash

# Ce script est utilisé pour démarrer l'API de classification de texte.
# Il charge les variables d'environnement et lance le serveur uvicorn.

# Charge les variables d'environnement depuis le fichier .env
# Le grep -v '^#' ignore les lignes commençant par # (commentaires)
# xargs transforme chaque ligne en argument pour la commande export
export $(grep -v '^#' .env | xargs)

# Lance le serveur uvicorn avec les paramètres suivants :
# - api.app.main:app : le chemin vers l'objet app FastAPI
# - --host 0.0.0.0 : permet l'accès depuis n'importe quelle adresse IP
# - --port 8000 : définit le port d'écoute du serveur
uvicorn api.app.main:app --host 0.0.0.0 --port 8000