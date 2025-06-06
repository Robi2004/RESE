import os

# Configuration réseau
HOST = "10.1.1.122"  # Adresse IP du serveur
PORT = 65432  # Port d'écoute

# Paramètres des logs
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_FILE = os.path.join(LOG_DIR, "server.log")

# Dossier contenant les fichiers modifiables
FILES_DIR = "files"
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

# Paramètres généraux
BUFFER_SIZE = 1024  # Taille du buffer pour les sockets
MAX_CONNECTIONS = 5  # Nombre max de connexions simultanées

# Codes d'erreur définis dans le projet
ERROR_MESSAGES = {
    "ERR_INVALID_REQUEST": "La requête est invalide ou mal formée.",
    "ERR_UNAUTHORIZED": "Vous n'avez pas les droits pour effectuer cette action.",
    "ERR_NOT_FOUND": "La ressource demandée est introuvable.",
    "ERR_SERVER_BUSY": "Le serveur est actuellement surchargé.",
    "ERR_INTERNAL": "Une erreur interne est survenue.",
    "ERR_PAYLOAD_TOO_LARGE": "Le payload dépasse la taille autorisée.",
    "ERR_FILE_NAME": "Le nom du fichier est incorrect."
}