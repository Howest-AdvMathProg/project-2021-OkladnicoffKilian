import logging
import socket

headersize = 128
encoding_format = 'utf-8'

class Client():
    def __init__(self, port, host=socket.gethostname()):
        self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.host = socket.gethostname()
        self.host = host
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
        logging.debug(f"Sending data {data}")
        data = data.encode(encoding_format)

        # calculate msg length
        msglength = len(data)
        msglength = str(msglength).encode(encoding_format)
        msglength += b' ' * (headersize - len(msglength))

        # send msglength and message
        self.socket_to_server.send(msglength)
        self.socket_to_server.send(data)

        logging.debug("Data sent")

    def receive_data(self):
        result = self.io_stream_server.readline().rstrip("\n")
        return result