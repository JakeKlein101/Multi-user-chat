import socket
# from _thread import *
# from threading import Thread

IP_ADDRESS = "127.0.0.1"
PORT = 8820
BUFFER_SIZE = 4096


class Message:
    def __init__(self, author, message):
        self._author = author
        self._message = message

    def __str__(self):
        print(f"The author is: {self._author}. The Message is: {self._message}")


class Room:
    def __init__(self):
        self._client_list = []

    def __str__(self):
        print("The clients in this room are: ")
        for x in self._client_list:
            print(x)


class Client:
    def __init__(self, sock, ip):
        self._client_sock = sock
        self._client_address = ip

    def start(self):
        received_content = self._client_sock.recv(BUFFER_SIZE)
        message = Message(received_content[0], received_content[1])

    def __str__(self):
        print(self._client_address)


class Server:
    def __init__(self, ip, port):
        self._address = ip
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._room_list = []

    def bind_server(self):
            self._sock.bind((self._address, self._port))
            self._sock.listen(1)

    def start_accepting(self):
        while True:
            client_socket, client_address = self._sock.accept()
            print(f"connected to {client_address}")
            client = Client(client_socket, client_address)


def main():
    my_server = Server(IP_ADDRESS, PORT)
    my_server.bind_server()


if __name__ == '__main__':
    main()