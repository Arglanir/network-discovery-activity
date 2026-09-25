import json
from collections import deque
from http.server import HTTPServer, BaseHTTPRequestHandler

# Stocke au maximum les 20 derniers messages
messages_store = deque(maxlen=20)

# Lecture de la page HTML à renvoyer
with open(__file__.replace('.py', '.html'), encoding='utf-8') as fin:
    HTML_PAGE = fin.read()

# Classe pour écouter les messages HTTP
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # 1 message "/": c'est la page d'accueil
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        
        # 2 message "/messages": pour renvoyer les messages qu'on a stockés
        elif self.path == '/messages':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            # Convertit les messages en liste JSON et les envoie
            messages_list = list(messages_store)
            self.wfile.write(json.dumps(messages_list).encode('utf-8'))

        else:
            self.send_error(404, "Page non trouvée")

    def do_POST(self):
        # 3 messages sur /message: quelqu'un nous a envoyé un message, à stocker.
        if self.path == '/message':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                author = data.get('author', 'Anonyme')
                text = data.get('text', '')

                if text:
                    messages_store.append({'author': author, 'text': text})
                    self.log_message("From %s: %r", author, text)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok'}).encode('utf-8'))

            except json.JSONDecodeError:
                self.send_error(400, "Données JSON invalides")
        else:
            self.send_error(404, "Endpoint non trouvé")

# Méthode principale avec une boucle infinie
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serveur démarré sur http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du serveur.")
        httpd.server_close()

if __name__ == '__main__':
    run()
