import socket
import pickle
from threading import Thread
import sys
import random

IP_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 8820
BUFFER_SIZE = 4096


class Message:
    def __init__(self, request_code, author, content, room_code=0):
        self._author = author
        self._content = content
        self._request_code = request_code
        self._room_code = room_code

    def get_request(self):
        return self._request_code

    def get_room_code(self):
        return self._room_code

    def generate_message(self):
        return tuple([self._request_code, self._author, self._content, self._room_code])

    def __str__(self):
        return f"{self._author}: {self._content}"


class Room:
    def __init__(self, room_id):
        self._client_list = []
        self._room_id = room_id

    def get_room_id(self):
        return self._room_id

    def append_to_room(self, client):
        self._client_list.append(client)

    def send_to_room_mates(self):
        for x in self._client_list:
            x.get_sock().send(pickle.dumps(message.generate_message()))

    def __str__(self):
        output = ""
        output += "The clients in this room are: "
        for x in self._client_list:
            output += x
            output += " -> "
        return output


class Client(Thread):
    def __init__(self, sock, ip, other_clients_list):
        Thread.__init__(self)
        self._client_sock = sock
        self._client_address = ip
        self._id = random.randint(0, 200000)
        self._other_clients_list = other_clients_list
        self._room_id = 0

    def get_id(self):
        return self._id

    def get_sock(self):
        return self._client_sock

    def run(self):
        try:
            self.receive_messages()
        except ConnectionResetError:
            print("Connection was forcibly closed")

    def send_messages(self, message):
        for x in self._other_clients_list:
            if x.get_id() != self._id:
                x.get_sock().send(pickle.dumps(message.generate_message()))

    def receive_messages(self):
        while True:
            encoded_content = self._client_sock.recv(BUFFER_SIZE)
            received_content = pickle.loads(encoded_content)
            message = Message(*received_content)
            print(message)
            self.send_messages(message)

    def __str__(self):
        return f"IP: {self._client_address}, ID: {self._id}"


class Server:
    def __init__(self):
        self._address = IP_ADDRESS
        self._port = PORT
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._room_list = []
        self._client_list = []

    def start(self):
            self._sock.bind((self._address, self._port))
            self._sock.listen(1)
            print(f"Server has been binded to the IP: {self._address} port: {self._port}")
            self.start_accepting()

    def start_accepting(self):
        print("The server started accepting")
        while True:
            client_socket, client_address = self._sock.accept()
            client = Client(client_socket, client_address, self._client_list)
            self._client_list.append(client)
            client.start()


def main():
    my_server = Server()
    my_server.start()


if __name__ == '__main__':
    main()
