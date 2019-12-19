import socket
# from _thread import *
# from threading import Thread

IP_ADDRESS = "127.0.0.1"
PORT = 8820


class Client:
    def __init__(self, sock, ip):
        self._client_sock = sock
        self._client_address = ip


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




def main():
    my_server = Server(IP_ADDRESS, PORT)
    my_server.bind_server()

if __name__ == '__main__':
    main()