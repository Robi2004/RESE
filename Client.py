import socket

def connect_to_server():
    """Permet de saisir l'IP et le port du serveur de manière dynamique."""
    host = input("Entrez l'adresse IP du serveur (ex: 192.168.1.100) : ").strip()
    if not host:
        host = "127.0.0.1"  # Par défaut, localhost

    try:
        port = int(input("Entrez le port du serveur (ex: 65432) : ").strip())
    except ValueError:
        print("⚠ Erreur : Le port doit être un nombre entier. Utilisation du port 65432 par défaut.")
        port = 65432  # Port par défaut

    return host, port


def send_request(host,port,command,payload):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        message = f"{command} {payload}".strip()
        client_socket.sendall(message.encode("utf-8"))

        response = client_socket.recv(1024).decode("utf-8")
        client_socket.close()

        return response
    except ConnectionRefusedError:
        return "Erreur : Impossible de se connecter au serveur"

# Interface CLI simple
if __name__ == "__main__":
    host, port = connect_to_server()
    while True:
        commandEnter = input("Commande (GET, SET, SEND, SYS, EXIT) : ").strip()
        command = commandEnter.split(":")[0].upper()
        
        if command == "EXIT":
            break
        elif command == "SET":
            filename = input("Nom du fichier : ").strip()
            content = input("Contenu : ").strip()
            payload = f"{filename}, {content}"
        else:
            payload = commandEnter.split(":", 1)[1].strip().upper() if ":" in commandEnter else ""
            
        print("Réponse :", send_request(host,port,command, payload))
    print("Réponse :", send_request(host,port,"EXIT", ""))