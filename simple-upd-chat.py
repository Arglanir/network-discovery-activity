import socket
import threading

PORT = 50000
BUFFER = []

# 1 Méthode pour stocker les messages qui arrivent sur le réseau
def ecouter_reseau(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            BUFFER.append(data.decode('utf-8'))
        except Exception:
            break

# 2 Création d'une socket réseau UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Permet de lancer plusieurs instances sur la même machine
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
except AttributeError:
    pass  # SO_REUSEPORT n'est pas disponible sur certains vieux Windows

# 3 On dit à l'ordinateur : je veux écouter sur ce port
sock.bind(('', PORT))

# 4 Puis on lance le petit programme d'écoute en arrière-plan
thread = threading.Thread(target=ecouter_reseau, args=(sock,), daemon=True)
thread.start()

# 5 On commence à se présenter au programme
pseudo = input("Ton nom : ")

print(f"--- Chat prêt sur le port {PORT} pour {pseudo} ---")

# 6 boucle principale : le programme attend qu'on entre un texte,
# puis affiche les réponses des autres
while True:
    texte = input()

    while BUFFER:
        print(BUFFER.pop(0))

    if texte.strip():
        msg_brut = f"{pseudo}: {texte}"
        # On envoie !
        sock.sendto(msg_brut.encode('utf-8'), ('127.255.255.255', PORT)) # <broadcast> est peut-être bloqué
