import socket
import pickle
from threading import Thread
import sys
import random

IP_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 8820
BUFFER_SIZE = 4096


class Message:
    def __init__(self, room_code, request_code, author="", content="", choice=0):
        self._author = author
        self._content = content
        self._request_code = request_code
        self._room_code = room_code
        self._choice = choice

    def get_choice(self):
        return self._choice

    def get_request(self):
        """
        the request code means: 1 - join room, 2 - create room
        :return: the request code that was transferred in the message
        """
        return self._request_code

    def get_room_code(self):
        """
        :return: returns the requested room code
        """
        return self._room_code

    def generate_message(self):
        """
        :return: a tuple of all the info that needs to be transferred
        """
        return tuple([self._room_code, self._request_code, self._author, self._content])

    def __str__(self):
        return f"{self._author}: {self._content}"


class Room:
    def __init__(self, room_id, client):
        self._client_list = [client]
        self._room_id = room_id

    def get_room_id(self):
        """
        :return: returns the room id of this specific instance of the room.
        """
        return self._room_id

    def get_client_list(self):
        """
        :return: returns a list of the clients connected to this specific instance of the room.
        """
        return self._client_list

    def append_to_room(self, client):
        """
        adds a client to the room list.
        :param client: Client
        """
        self._client_list.append(client)

    def __str__(self):
        output = ""
        output += "The clients in this room are: "
        for x in self._client_list:
            output += str(x.get_id())
            output += " -> "
        output += f"The room id is: {self._room_id}"
        return output


class Client(Thread):
    def __init__(self, sock, ip, other_clients_list, server, is_admin=False):
        Thread.__init__(self)
        self._client_sock = sock
        self._client_address = ip
        self._id = random.randint(0, 20000000)
        self._other_clients_list = other_clients_list
        self._room_id = 0
        self._room = None
        self._host = server
        self._is_admin = is_admin

    def get_id(self):
        """
        the id is a random number that is used to differentiate between clients.
        :return: returns the id of this specific instance of the client
        """
        return self._id

    def get_sock(self):
        """
        :return: returns this specific client's socket object
        """
        return self._client_sock

    def run(self):
        """
        run overrides the thread method run which is inherited from Thread.
        This method starts a new thread every time its called.
        """
        try:
            self.receive_messages()
        except ConnectionResetError:
            print("Connection was forcibly closed")

    def send_messages(self, message):
        """
        sends the specific message to all the clients in the room of this specific instance of the client
        :param message: Message
        """
        for x in self._room.get_client_list():
            if x.get_id() != self._id:
                x.get_sock().send(pickle.dumps(message.generate_message()))

    def receive_initial_message(self):
        """
        Receives the initial message the sorts the clients request.
        It creates/puts him in the room he requested/ wanted to create.
        """
        initial_packet = pickle.loads(self._client_sock.recv(BUFFER_SIZE))
        initial_info = Message(*initial_packet)
        print(f"The requested room id: {initial_info.get_room_code()}")
        if initial_info.get_request() == 2:
            room = Room(initial_info.get_room_code(), self)
            self._room = room
            self._host.update_room_list(room)
            self._is_admin = True
            print(self)
        elif initial_info.get_request() == 1:
            for x in self._host.get_room_list():
                if x.get_room_id() == initial_info.get_room_code():
                    x.append_to_room(self)
                    self._room = x
                    print(self)
        else:
            print("invalid request code")

    def receive_messages(self):
        """
        receives all the messages from the client side.
        Calls the send_messages method to send the received message to all the other clients in the room.
        """
        self.receive_initial_message()
        while True:
            encoded_content = self._client_sock.recv(BUFFER_SIZE)
            received_content = pickle.loads(encoded_content)
            message = Message(*received_content)
            print(message.get_choice())
            if message.get_choice() != 0 and self._is_admin: # needs fixing
                self.handle_command(message.get_choice())
            self.send_messages(message)

    def handle_command(self, choice_code):  # needs fixing
        if choice_code == 1:
            data = tuple(self._room.get_client_list())
            self._client_sock.send(pickle.dumps(data))

    def __str__(self):
        return f"IP: {self._client_address}, ID: {self._id}, Is admin: {self._is_admin}"


class Server:
    def __init__(self):
        self._address = IP_ADDRESS
        self._port = PORT
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._room_list = []
        self._client_list = []

    def update_room_list(self, room):
        """
        adds a room to the room list
        :param room: Room
        """
        self._room_list.append(room)

    def get_room_list(self):
        """
        :return: returns a list of all the rooms that are opened in the server.
        """
        return self._room_list

    def start(self):
        """
        binds the server and calls start_accepting
        """
        self._sock.bind((self._address, self._port))
        self._sock.listen(1)
        print(f"Server has been binded to the IP: {self._address} port: {self._port}")
        self.start_accepting()

    def start_accepting(self):
        """
        accepts clients and creates a new instance of a client for each one.
        Then initiates a client thread with start().
        """
        print("The server started accepting")
        while True:
            client_socket, client_address = self._sock.accept()
            print(f"{client_address} just connected")
            client = Client(client_socket, client_address, self._client_list, self)
            self._client_list.append(client)
            client.start()


def main():
    my_server = Server()
    my_server.start()


if __name__ == '__main__':
    main()
