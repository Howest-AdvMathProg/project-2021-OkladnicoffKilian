import logging
import socket

class Client():
    def __init__(self, port):
        self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = port
    
    def connect(self):
        self.socket_to_server.connect((self.host, self.port))
        logging.info("Connected to server")

    def disconnect(self):
        self.socket_to_server.close()
        logging.info("Connection closed with server")