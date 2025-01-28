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

        valid, response = utils.validate_request(data)
        if not valid:
            utils.log_error(f"❌ Requête invalide de {addr}: {data}")
            client_socket.sendall(response.encode("utf-8"))
            return

        command, payload = response
        response = "ERR_INVALID_REQUEST"

        if command == "INFO":
            utils.log_message(f"📌 INFO demandé: {payload} de {addr}")
            if payload == "DATE":
                response = datetime.datetime.now().strftime("%Y-%m-%d")
            elif payload == "TIME":
                response = datetime.datetime.now().strftime("%H:%M:%S")
            elif payload == "IP":
                response = config.HOST
            elif payload == "PORT":
                response = str(config.PORT)

        elif command == "MESSAGE":
            utils.log_message(f"💬 MESSAGE reçu de {addr}: {payload}")
            response = f"Message reçu: {payload}"

        elif command == "SYSTEM":
            utils.log_message(f"⚙ SYSTEM demandé: {payload} de {addr}")
            if payload == "STATUS":
                response = f"CPU: {psutil.cpu_percent()}%, RAM: {psutil.virtual_memory().percent}%"

        elif command == "UPDATE":
            utils.log_message(f"📝 UPDATE demandé de {addr}: {payload}")
            try:
                filename, content = payload.split(", ")
                response = utils.save_to_file(filename, content)
            except Exception:
                response = utils.get_error_message("ERR_INVALID_REQUEST")

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
