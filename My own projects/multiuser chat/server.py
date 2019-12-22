import socket
import pickle
from threading import Thread
import sys
import random

IP_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 8820
BUFFER_SIZE = 4096


class Message:
    def __init__(self, request_code, author, content):
        self._author = author
        self._content = content
        self._request_code = request_code

    def generate_message(self):
        return tuple([self._request_code, self._author, self._content])

    def __str__(self):
        return f"{self._author}: {self._content}"


class Room:
    def __init__(self):
        self._client_list = []

    def __str__(self):
        output = ""
        output += "The clients in this room are: "
        for x in self._client_list:
            output += x
        return output


class Client(Thread):
    def __init__(self, sock, ip, other_clients_list):
        Thread.__init__(self)
        self._client_sock = sock
        self._client_address = ip
        self._id = random.randint(0, 200000)
        self._other_clients_list = other_clients_list

    def get_id(self):
        return self._id

    def get_sock(self):
        return self._client_sock

    def run(self):
        self.receive_messages()

    def receive_messages(self):
        name = self._client_sock.recv(BUFFER_SIZE).decode()
        print(f"{name} just connected to this room! Be nice and say hi")
        while True:
            encoded_content = self._client_sock.recv(BUFFER_SIZE)
            received_content = pickle.loads(encoded_content)
            message = Message(*received_content)
            print(message)
            for x in self._other_clients_list:
                print(x)
            for x in self._other_clients_list:
                if x.get_id() != self._id:
                    x.get_sock().send(pickle.dumps(message.generate_message()))

    def __str__(self):
        return f"IP: {self._client_address}, ID: {self._id}"


class Server:
    def __init__(self, ip, port):
        self._address = ip
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._room_list = []
        self._client_list = []

    def bind_server(self):
            self._sock.bind((self._address, self._port))
            self._sock.listen(1)
            print(f"Server has been binded to the IP: {self._address} port: {self._port}")

    def start_accepting(self):
        print("The server started accepting")
        while True:
            client_socket, client_address = self._sock.accept()
            client = Client(client_socket, client_address, self._client_list)
            self._client_list.append(client)
            client.start()


def main():
    my_server = Server(IP_ADDRESS, PORT)
    my_server.bind_server()
    my_server.start_accepting()


if __name__ == '__main__':
    main()