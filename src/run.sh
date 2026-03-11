#!/bin/bash
# run.sh : lance la GUI du planificateur ferroviaire
# Assurez-vous que ce script est exécutable : chmod +x run.sh

# Aller dans le dossier du script pour que les chemins relatifs fonctionnent
cd "$(dirname "$0")"

# Lancer l'application Python
python3 gui.py
