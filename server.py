import socket
import config
import utils
import datetime
import os
import psutil
import threading

def handle_client(client_socket, addr):
    """Gère la connexion avec un client spécifique."""
    utils.log_message(f"🔗 Connexion établie avec {addr}")

    try:
        data = client_socket.recv(config.BUFFER_SIZE).decode("utf-8").strip()
        if not data:
            return

        # Traitement de la commande côté serveur
        if ":" in data:
            command, payload = data.split(":", 1)
            command = command.strip().upper()
            payload = payload.strip().upper()
        else:
            command = data.strip().upper()
            payload = ""

        response = "ERR_INVALID_REQUEST"

        match command:
            case "EXIT":
                utils.log_message(f"🔌 Connexion fermée avec {addr}")
                response = "Au revoir!"
                client_socket.sendall(response.encode("utf-8"))
                client_socket.close()
                return
            case "GET":
                utils.log_message(f"📌 INFO demandé: {payload} de {addr}")
                match payload:
                    case "DATE":
                        response = datetime.datetime.now().strftime("%Y-%m-%d")
                    case "TIME":
                        response = datetime.datetime.now().strftime("%H:%M:%S")
                    case "IP":
                        response = config.HOST
                    case "PORT":
                        response = str(config.PORT)
            case "SEND":
                utils.log_message(f"💬 MESSAGE reçu de {addr}: {payload}")
                response = f"Message reçu: {payload}"
            case "SYS":
                utils.log_message(f"⚙ SYSTEM demandé: {payload} de {addr}")
                if payload == "STATUS":
                    response = f"CPU: {psutil.cpu_percent()}%, RAM: {psutil.virtual_memory().percent}%"
            case "SET":
                utils.log_message(f"📝 UPDATE demandé de {addr}: {payload}")
                try:
                    parts = payload.split(", ", 1)
                    if len(parts) != 2:
                        response = utils.get_error_message("ERR_INVALID_REQUEST")
                    else:
                        filename = parts[0].strip().lower()
                        content = parts[1]
                        response = utils.save_to_file(filename, content)
                except Exception:
                    response = utils.get_error_message("ERR_INVALID_REQUEST")

        client_socket.sendall(response.encode("utf-8"))
    
    except Exception as e:
        utils.log_error(f"🚨 Erreur avec {addr}: {e}")

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