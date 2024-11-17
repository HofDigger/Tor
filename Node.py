import socket
from Crypto.Cipher import AES

class Node:
    def __init__(self, port, next_node_address=None, key=None):
        self.port = port
        self.next_node_address = next_node_address
        self.key = key

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', self.port))
        server_socket.listen(1)
        print(f"Node listening on port {self.port}")

        while True:
            client_socket, _ = server_socket.accept()
            data = client_socket.recv(4096)
            next_address, message_content = self.decrypt_data(data)

            if self.next_node_address:
                # Forward message to the next node
                next_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                next_socket.connect(self.next_node_address)
                next_socket.send(message_content)

                # Receive the response from the next node
                response = next_socket.recv(4096)
                next_socket.close()

                # Encrypt the response and send it back
                client_socket.send(self.encrypt_data(response))
            else:
                # Pass the message to the exit node
                client_socket.send(message_content)

            client_socket.close()

    def decrypt_data(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = data[:16]
        encrypted_data = data[16:]
        decrypted_data = cipher.decrypt_and_verify(encrypted_data, nonce)
        next_address, message = decrypted_data.decode().split('|', 1)
        next_host, next_port = next_address.split(':')
        return (next_host, int(next_port)), message.encode()

    def encrypt_data(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        encrypted_data, tag = cipher.encrypt_and_digest(data)
        return nonce + encrypted_data
