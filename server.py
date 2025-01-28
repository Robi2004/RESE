import socket
import config
import utils
import datetime
import os
import psutil
import threading

HELP_MESSAGE = """\
REPONSE : BIENVENUE
Bienvenue sur le serveur Winsocket !

📌 Commandes disponibles :
- INFO : DATE       → Obtenir la date actuelle
- INFO : TIME       → Obtenir l'heure actuelle
- INFO : IP         → Obtenir l'adresse IP du serveur
- INFO : PORT       → Obtenir le port du serveur

- MESSAGE : <texte> → Envoyer un message au serveur

- SYSTEM : STATUS   → Voir l'état du CPU et de la mémoire
- UPDATE : <fichier, contenu> → Modifier un fichier

- HELP            → Voir ce message d'aide

Envoyez votre première commande pour commencer.
"""

def format_response(tag, content):
    """Formate une réponse selon le protocole défini."""
    return f"{tag} : {content}"

def handle_client(client_socket, addr):
    """Gère la connexion avec un client spécifique."""
    utils.log_message(f"🔗 Connexion établie avec {addr}")

    try:
        while True:
            # Attendre une requête du client
            data = client_socket.recv(config.BUFFER_SIZE).decode("utf-8").strip()
            if not data:
                break

            valid, response = utils.validate_request(data)
            if not valid:
                utils.log_error(f"❌ Requête invalide de {addr}: {data}")
                client_socket.sendall(format_response("ERREUR", "Commande inconnue. Tapez HELP pour voir les commandes disponibles.").encode("utf-8"))
                continue

            command, payload = response
            response = format_response("ERREUR", "Commande inconnue. Tapez HELP pour voir les commandes disponibles.")  # Valeur par défaut

            if command == "INFO":
                utils.log_message(f"📌 INFO demandé: {payload} de {addr}")
                if payload == "DATE":
                    response = format_response("REPONSE", datetime.datetime.now().strftime('%Y-%m-%d'))
                elif payload == "TIME":
                    response = format_response("REPONSE", datetime.datetime.now().strftime('%H:%M:%S'))
                elif payload == "IP":
                    response = format_response("REPONSE", config.HOST)
                elif payload == "PORT":
                    response = format_response("REPONSE", str(config.PORT))

            elif command == "MESSAGE":
                utils.log_message(f"💬 MESSAGE reçu de {addr}: {payload}")
                response = format_response("REPONSE", f"Message reçu: {payload}")

            elif command == "SYSTEM":
                utils.log_message(f"⚙ SYSTEM demandé: {payload} de {addr}")
                if payload == "STATUS":
                    response = format_response("REPONSE", f"CPU : {psutil.cpu_percent()}%, RAM : {psutil.virtual_memory().percent}%")

            elif command == "UPDATE":
                utils.log_message(f"📝 UPDATE demandé de {addr}: {payload}")
                try:
                    filename, content = payload.split(", ")
                    response = format_response("REPONSE", utils.save_to_file(filename, content))
                except Exception:
                    response = format_response("ERREUR", "ERR_INVALID_REQUEST")

            elif command == "HELP":
                response = HELP_MESSAGE

            client_socket.sendall(response.encode("utf-8"))

    except Exception as e:
        utils.log_error(f"🚨 Erreur avec {addr}: {e}")

    finally:
        client_socket.close()
        utils.log_message(f"🔌 Connexion fermée avec {addr}")

def start_server():
    """Démarre le serveur Winsocket et gère plusieurs connexions."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((config.HOST, config.PORT))
        server_socket.listen(config.MAX_CONNECTIONS)
        utils.log_message(f"✅ Serveur Winsocket en écoute sur {config.HOST}:{config.PORT}...")

        while True:
            client_socket, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.start()

    except OSError as e:
        utils.log_error(f"🚨 Erreur sur le port {config.PORT}: {e}")

    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
