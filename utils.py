import logging
import config
import os
import sys

# Configuration du logging avec écriture immédiate et affichage en console
logger = logging.getLogger("server_logger")
logger.setLevel(logging.INFO)

# Handler pour écrire les logs dans un fichier
file_handler = logging.FileHandler(config.LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)

# Handler pour afficher les logs en direct dans la console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(file_formatter)

# Ajout des handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_message(message):
    """Enregistre un message dans le fichier de logs et force l'écriture immédiate."""
    logger.info(message)
    file_handler.flush()  # Force l'écriture immédiate

def log_error(error):
    """Enregistre une erreur dans le fichier de logs et force l'écriture immédiate."""
    logger.error(error)
    file_handler.flush()  # Force l'écriture immédiate

def get_error_message(error_code):
    """Retourne le message d'erreur associé à un code d'erreur."""
    return config.ERROR_MESSAGES.get(error_code, "Erreur inconnue.")

def validate_request(data):
    """Valide la requête reçue et retourne True si correcte, sinon un code d'erreur."""
    parts = data.strip().split(" ", 1)
    if len(parts) < 2:
        return False, "ERR_INVALID_REQUEST"
    return True, (parts[0].upper(), parts[1])

def save_to_file(filename, content):
    """Écrit du contenu dans un fichier dans le dossier files/."""
    file_path = os.path.join(config.FILES_DIR, filename)
    try:
        with open(file_path, "w") as f:
            f.write(content)
        log_message(f"Fichier {filename} mis à jour.")
        return "Fichier mis à jour avec succès"
    except Exception as e:
        log_error(f"Erreur lors de l'écriture du fichier {filename}: {e}")
        return "ERR_INTERNAL"