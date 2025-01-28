import socket
import config
import utils
import datetime
import os
import psutil

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((config.HOST, config.PORT))
        server_socket.listen(config.MAX_CONNECTIONS)
        utils.log_message(f"Serveur Winsocket en écoute sur {config.HOST}:{config.PORT}...")

        while True:
            client_socket, addr = server_socket.accept()
            utils.log_message(f"Connexion établie avec {addr}")

            data = client_socket.recv(config.BUFFER_SIZE).decode("utf-8").strip()
            if not data:
                client_socket.close()
                continue  # Ignorer les requêtes vides

            valid, response = utils.validate_request(data)
            if not valid:
                utils.log_error(f"Requête invalide de {addr}: {data}")
                client_socket.sendall(response.encode("utf-8"))
                client_socket.close()
                continue

            command, payload = response
            response = "ERR_INVALID_REQUEST"  # Valeur par défaut

            if command == "INFO":
                if payload == "DATE":
                    response = datetime.datetime.now().strftime("%Y-%m-%d")
                elif payload == "TIME":
                    response = datetime.datetime.now().strftime("%H:%M:%S")
                elif payload == "IP":
                    response = config.HOST
                elif payload == "PORT":
                    response = str(config.PORT)

            elif command == "MESSAGE":
                response = f"Message reçu: {payload}"

            elif command == "SYSTEM":
                if payload == "STATUS":
                    response = f"CPU: {psutil.cpu_percent()}%, RAM: {psutil.virtual_memory().percent}%"
                elif payload == "RESTART":
                    response = "Redémarrage en cours..."  # À implémenter

            elif command == "UPDATE":
                try:
                    filename, content, new_name = payload.split(", ")
                    if new_name:
                        os.rename(os.path.join(config.FILES_DIR, filename), os.path.join(config.FILES_DIR, new_name))
                    if content:
                        response = utils.save_to_file(filename, content)
                except Exception:
                    response = utils.get_error_message("ERR_INVALID_REQUEST")

            client_socket.sendall(response.encode("utf-8"))
            client_socket.close()
    
    except OSError as e:
        utils.log_error(f"Erreur sur le port {config.PORT}: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
