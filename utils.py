import logging
import config
import datetime
import os

# Configuration du logging
logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_message(message):
    """Enregistre un message dans le fichier de logs."""
    print(message)  # Affiche aussi dans la console
    logging.info(message)

def log_error(error):
    """Enregistre une erreur dans le fichier de logs."""
    print(f"ERREUR: {error}")
    logging.error(error)

def get_error_message(error_code):
    """Retourne le message d'erreur associé à un code d'erreur."""
    return config.ERROR_MESSAGES.get(error_code, "Erreur inconnue.")

def validate_request(data):
    """Valide la requête reçue et retourne True si correcte, sinon un code d'erreur."""
    parts = data.strip().split(" ", 1)
    if len(parts) < 2:
        return False, "ERR_INVALID_REQUEST"
    
    return True, (parts[0].upper(), parts[1])  # Assure que la commande est en majuscules

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
