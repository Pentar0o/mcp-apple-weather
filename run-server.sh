#!/bin/bash

# Script de lancement pour le serveur MCP Apple Weather
# Ce script configure l'environnement et lance le serveur Python

# Configuration des chemins Python
# Ajuste ces chemins selon ton installation Python
export PATH="/opt/homebrew/opt/python@3.12/libexec/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export PYTHONPATH="/opt/homebrew/lib/python3.12/site-packages:$PYTHONPATH"

# Se placer dans le répertoire du script
# Cela permet de lancer le serveur depuis n'importe où
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Vérifier que le fichier .env existe
if [ ! -f ".env" ]; then
    echo "Erreur : Le fichier .env n'existe pas."
    echo "Copiez .env.example vers .env et configurez vos identifiants Apple."
    exit 1
fi

# Vérifier que le dossier certificats existe
if [ ! -d "certificats" ]; then
    echo "Erreur : Le dossier certificats/ n'existe pas."
    echo "Créez le dossier et ajoutez vos certificats .p8"
    exit 1
fi

# Lancer le serveur Python
# Le exec remplace le processus bash par Python pour une meilleure gestion des signaux
exec python3 server.py