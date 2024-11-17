import socket
from Crypto.Cipher import AES

class Client:
    def __init__(self, nodes):
        self.nodes = nodes

    def send_message(self, query):
        data = query.encode()
        for node in reversed(self.nodes):
            data = self.encrypt_data(data, node['key'], node['address'])

        first_node_address = self.nodes[0]['address']
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(first_node_address)
        sock.send(data)


        response = sock.recv(4096)
        sock.close()


        for node in self.nodes:
            response = self.decrypt_data(response, node['key'])

        print("Final response:", response.decode())

    def encrypt_data(self, data, key, next_address):
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        encrypted_data, tag = cipher.encrypt_and_digest(f"{next_address[0]}:{next_address[1]}|".encode() + data)
        return nonce + encrypted_data

    def decrypt_data(self, data, key):
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = data[:16]
        encrypted_data = data[16:]
        decrypted_data = cipher.decrypt_and_verify(encrypted_data, nonce)
        return decrypted_data
