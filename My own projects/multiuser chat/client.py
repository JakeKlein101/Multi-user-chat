import socket
import pickle
from threading import Thread
import sys

IP_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 8820
BUFFER_SIZE = 4096


class Message:
    def __init__(self, request_code, author, content):
        self._request_code = request_code
        self._author = author
        self._content = content

    def generate_message(self):
        return tuple([self._request_code, self._author, self._content])


class Client:
    def __init__(self, name):
        self._request_code = 0
        self._name = name
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self._sock.connect((IP_ADDRESS, PORT))

    def start_requesting(self):
        print("would you like to:")
        print("1 - join room")
        print("2 - create room")
        self._request_code = int(input())
        print("Welcome to the room! you can start talking with your friends here:")
        while True:
            content = input()
            message = Message(self._request_code, self._name, content)
            self._sock.send(pickle.dumps(message.generate_message()))


def main():
    print("Welcome to the 'Han'! the first global mutli - user room!")
    client_name = input("Please Write down your name:")
    print(f"Welcome {client_name}!")
    client = Client(client_name)
    client.start()
    client.start_requesting()


if __name__ == '__main__':
    main()