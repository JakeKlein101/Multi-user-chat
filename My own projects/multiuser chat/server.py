import socket
import pickle
from threading import Thread
import sys

IP_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 8820
BUFFER_SIZE = 4096


class Message:
    def __init__(self, author, message):
        self._author = author
        self._message = message

    def get_author(self):
        return self._author

    def __str__(self):
        return f"{self._author}: {self._message}"


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
    def __init__(self, sock, ip):
        Thread.__init__(self)
        self._client_sock = sock
        self._client_address = ip

    def run(self):
        self.receive_messages()

    def receive_messages(self):
        done = False
        while True:
            encoded_content = self._client_sock.recv(BUFFER_SIZE)
            received_content = pickle.loads(encoded_content)
            message = Message(received_content[1], received_content[2])
            while not done:  # emulates Do while
                print(f"{message.get_author()} just connected to this room! Be nice and say hi")
                break
            done = True
            print(message)

    def __str__(self):
        return f"IP: {self._client_address}"


class Server:
    def __init__(self, ip, port):
        self._address = ip
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._room_list = []

    def bind_server(self):
            self._sock.bind((self._address, self._port))
            self._sock.listen(1)
            print(f"Server has been binded to the IP: {self._address} port: {self._port}")

    def start_accepting(self):
        print("The server started accepting")
        while True:
            client_socket, client_address = self._sock.accept()
            client = Client(client_socket, client_address)
            client.start()


def main():
    my_server = Server(IP_ADDRESS, PORT)
    my_server.bind_server()
    my_server.start_accepting()


if __name__ == '__main__':
    main()