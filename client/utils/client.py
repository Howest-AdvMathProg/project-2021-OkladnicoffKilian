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

        # create stream
        self.io_stream_server = self.socket_to_server.makefile(mode='rw')

    def disconnect(self):
        self.socket_to_server.close()
        logging.info("Connection closed with server")

    def send_data(self, data):
        self.io_stream_server.write(f"{data}\n")
        self.io_stream_server.flush()

    def receive_data(self):
        result = self.io_stream_server.readline().rstrip("\n")
        return result