# Acadêmica: Beatriz Avanzi Ecli    RA: 108612

# Sistema Distribuído de Votação simples que faz troca de mensagens usando TCP.
# Cada nó do sistema é uma máquina que possui um identificador, um endereço IP e uma porta.
# Na main emulamos 3 nós e cada um deles vota em uma opção diferente. Para cada voto, o nó envia uma mensagem para os outros nós.
# Para garantir que o sistema continue funcionando mesmo se uma das máquinas falhar, é usada a técnica de replicação de votos.
# Cada nó mantém uma lista com os votos recebidos dos outros nós e, quando um nó precisa saber o resultado da votação, 
# ele pergunta para os outros nós.

import socket
import threading

class Node:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port
        self.votes = {}
        self.lock = threading.Lock()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(5)
        print(f"Node {self.id} listening on {self.ip}:{self.port}")
        while True:
            conn, addr = self.socket.accept()
            threading.Thread(target=self.handle_request, args=(conn,)).start()

    def handle_request(self, conn):
        data = conn.recv(1024).decode()
        if data.startswith("VOTE"):
            vote = data.split()[1]
            with self.lock:
                self.votes[vote] = self.votes.get(vote, 0) + 1
            print(f"Node {self.id} voted for {vote}")
        elif data == "STATUS":
            with self.lock:
                conn.sendall(str(len(self.votes)).encode())
        conn.close()

    def vote(self, vote):
        for node in nodes:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((node.ip, node.port))
                sock.sendall(f"VOTE {vote}".encode())
                sock.close()
            except Exception as e:
                print(f"Failed to vote for {vote} at {node.ip}:{node.port}: {e}")

    def get_status(self):
        count = 0
        for node in nodes:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((node.ip, node.port))
                sock.sendall("STATUS".encode())
                with self.lock:
                    count += int(sock.recv(1024).decode())
                sock.close()
            except Exception as e:
                print(f"Failed to get status from {node.ip}:{node.port}: {e}")
        return count

nodes = [
    Node(1, "localhost", 8001),
    Node(2, "localhost", 8002),
    Node(3, "localhost", 8003),
]

def start_nodes():
    for node in nodes:
        threading.Thread(target=node.start).start()


if __name__ == "__main__":
    start_nodes()
    nodes[0].vote("option1")
    nodes[1].vote("option1")
    nodes[2].vote("option2")
    print(nodes[0].get_status())