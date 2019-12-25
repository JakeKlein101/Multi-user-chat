import socket
import pickle
import sys
from threading import Thread


IP_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 8820
BUFFER_SIZE = 4096


class Message:
    def __init__(self, room_code, request_code, author="", content=""):
        self._request_code = request_code
        self._author = author
        self._content = content
        self._room_code = room_code

    def generate_message(self):
        return tuple([self._room_code, self._request_code, self._author, self._content])

    def generate_initial(self):
        return tuple([self._room_code, self._request_code])

    def __str__(self):
        return f"{self._author}: {self._content}"


class Client:
    def __init__(self, name):
        self._request_code = 0
        self._name = name
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._room_code = 0

    def start(self):
        self._sock.connect((IP_ADDRESS, PORT))
        self.start_requesting()

    def receiving(self):
        try:
            while True:
                received = pickle.loads(self._sock.recv(BUFFER_SIZE))
                received_message = Message(*received)
                print(received_message)
        except ConnectionResetError:
            print("The server crashed")

    def sending(self):
        while True:
            content = input()
            message = Message(self._room_code, self._request_code, self._name, content)
            self._request_code = 0
            self._sock.send(pickle.dumps(message.generate_message()))

    def start_requesting(self):
        print("would you like to:")
        print("1 - join room")
        print("2 - create room")
        self._request_code = int(input())
        if self._request_code == 2:
            print("What is the id of the room you want to create?")
            self._room_code = int(input())
        elif self._request_code == 1:
            print("What is the id of the room you want to join?")
            self._room_code = int(input())
        initial_info = Message(self._room_code, self._request_code)
        self._sock.send(pickle.dumps(initial_info.generate_initial()))
        print("Welcome to the room! you can start talking with your friends here:")
        recv_thread = Thread(target=self.receiving)
        send_thread = Thread(target=self.sending)
        recv_thread.start()
        send_thread.start()
        recv_thread.join()
        send_thread.join()


def main():
    print("Welcome to the 'Han'! the first global mutli - user room!")
    client_name = input("Please Write down your name:")
    print(f"Welcome {client_name}!")
    client = Client(client_name)
    client.start()


if __name__ == '__main__':
    main()