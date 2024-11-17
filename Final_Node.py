import socket
import requests

class ExitNode:
    def __init__(self, port):
        self.port = port

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))
        server_socket.listen(1)
        print(f"Exit Node listening on port {self.port}")

        while True:
            client_socket, _ = server_socket.accept()
            query = client_socket.recv(1024).decode()
            response = self.handle_request(query)

            # Send response back to the previous node
            client_socket.send(response.encode())
            client_socket.close()

    def handle_request(self, query):
        search_url = f"https://duckduckgo.com/?q={query}"
        response = requests.get(search_url)
        if response.status_code == 200:
            return response.text[:500]  # חלק מהתוצאה
        else:
            return "Failed to retrieve search results."
