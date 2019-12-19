import socket
import pickle
from _thread import *
from threading import Thread

IP_ADDRESS = "127.0.0.1"
PORT = 8820
BUFFER_SIZE = 4096


def main():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((IP_ADDRESS, PORT))
    message = (1, "jake", "hello")
    client_sock.send(pickle.dumps(message))



if __name__ == '__main__':
    main()