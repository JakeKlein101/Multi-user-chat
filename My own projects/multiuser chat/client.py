import socket
import pickle
import sys
from threading import Thread


IP_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 8820
BUFFER_SIZE = 4096


class Message:
    def __init__(self, room_code, request_code, author="", content="", choice=0):
        self._request_code = request_code
        self._author = author
        self._content = content
        self._room_code = room_code
        self._choice = choice

    def generate_message(self):
        """
        :return: returns a tuple that contains all the info that needs to ne transferred.
        """
        return tuple([self._room_code, self._request_code, self._author, self._content, self._choice])

    def generate_initial(self):
        """
        :return: returns a tuple of all the info that is needed for an initial message.
        """
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
        """
        connects the client to the server and initiates start_requesting.
        """
        self._sock.connect((IP_ADDRESS, PORT))
        self.start_requesting()

    def receiving(self):
        """
        receives all the messages sent from the server. Generates a Message object for each one with tuple unpacking.
        Then prints the received message.
        """
        try:
            while True:
                received = pickle.loads(self._sock.recv(BUFFER_SIZE))
                received_message = Message(*received)
                print(received_message)
        except ConnectionResetError:
            print("The server crashed")

    @staticmethod
    def menu():
        print("Welcome to the menu. Here are the available actions:")
        print("1 - declare somebody as admin")
        choice = int(input())
        return choice

    def handle_command(self, choice):  # needs fixing
        if choice == 1:
            people_in_group = pickle.loads(self._sock.recv(BUFFER_SIZE))
            print("who do you want to make admin?")
            for x in people_in_group:
                print(x)
            to_admin = input()
            self._sock.send(to_admin.encode())

    def sending(self):
        """
        Takes an input from the user(the content of the message), creates a Message object for it and then generates
        a message with the generate_message method. Then it encodes the tuple with pickle and sends it.
        """
        while True:
            content = input()
            if content == "//":  # needs fixing
                choice = self.menu()
                message = Message(self._room_code, self._request_code, self._name, content, choice)
                self._request_code = 0
                self._sock.send(pickle.dumps(message.generate_message()))
                self.handle_command(choice)
            else:
                message = Message(self._room_code, self._request_code, self._name, content)
                self._request_code = 0
                self._sock.send(pickle.dumps(message.generate_message()))

    def start_requesting(self):
        """
        1. Takes an input from the user for his request and the room code for  the room he wants to join/create.
        2. It generates and sends the initial message with the request code and room id.
        3. It starts and joins 2 threads for the function sending and receiving.
        4. It joins the Threads which makes the two functions run at the same time.
        """
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