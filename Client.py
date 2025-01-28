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

def send_request(host, port, message):
    """Envoie une requête au serveur et affiche la réponse."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Recevoir le message de bienvenue du serveur
        welcome_message = client_socket.recv(1024).decode("utf-8")
        print("\n🌍 Réponse du serveur :\n" + welcome_message)

        # Envoyer la requête de l'utilisateur
        client_socket.sendall(message.encode("utf-8"))

        # Recevoir la réponse du serveur
        response = client_socket.recv(1024).decode("utf-8")
        client_socket.close()

        return response
    except ConnectionRefusedError:
        return "❌ Erreur : Impossible de se connecter au serveur."

if __name__ == "__main__":
    # Demander à l'utilisateur de saisir l'IP et le port du serveur
    host, port = connect_to_server()

    while True:
        command = input("\n📝 Entrez votre commande (ou tapez EXIT pour quitter) : ").strip()
        if command.upper() == "EXIT":
            print("🔌 Déconnexion...")
            break

        response = send_request(host, port, command)
        print("\n📩 Réponse du serveur :\n" + response)
