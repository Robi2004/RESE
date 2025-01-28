import socket

# Configuration du serveur
HOST = "10.1.1.112"
PORT = 65432

def send_request(command, payload=""):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))

        message = f"{command} {payload}".strip()
        client_socket.sendall(message.encode("utf-8"))

        response = client_socket.recv(1024).decode("utf-8")
        client_socket.close()

        return response
    except ConnectionRefusedError:
        return "Erreur : Impossible de se connecter au serveur"

# Interface CLI simple
if __name__ == "__main__":
    while True:
        command = input("Commande (INFO, MESSAGE, SYSTEM, UPDATE, EXIT) : ").strip()
        if command.upper() == "EXIT":
            break
        payload = input("Payload : ").strip()
        print("Réponse :", send_request(command, payload))
