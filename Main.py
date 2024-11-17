from Node import Node
from Final_Node import ExitNode
from Client import Client
import threading
import os

if __name__ == "__main__":

    nodes = [
        {'address': ('localhost', 8001), 'key': os.urandom(16)},
        {'address': ('localhost', 8002), 'key': os.urandom(16)},
        {'address': ('localhost', 8003), 'key': os.urandom(16)}
    ]


    node1 = Node(port=8001, next_node_address=('localhost', 8002), key=nodes[0]['key'])
    node2 = Node(port=8002, next_node_address=('localhost', 8003), key=nodes[1]['key'])
    exit_node = ExitNode(port=8003)


    threading.Thread(target=node1.start, daemon=True).start()
    threading.Thread(target=node2.start, daemon=True).start()
    threading.Thread(target=exit_node.start, daemon=True).start()


    client = Client(nodes)
    query = "How does onion routing work?"
    print(f"Sending query: {query}")
    client.send_message(query)
