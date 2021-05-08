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
        self.session_id = None
    
    def connect(self):
        self.socket_to_server.connect((self.host, self.port))
        logging.info("Connected to server")

        # create stream
        # self.io_stream_server = self.socket_to_server.makefile(mode='rw')

    def disconnect(self):
        self.socket_to_server.close()
        logging.info("Connection closed with server")

    def send_data(self, data):
        # if client has a sessionid it needs to be send aswell
        logging.debug(f"Session id: {self.session_id}")
        if self.session_id != None:
            data += f"&session_id={self.session_id}"
            
        data = data.encode(encoding_format)

        # calculate msg length
        msglength = len(data)
        msglength = str(msglength).encode(encoding_format)
        msglength += b' ' * (headersize - len(msglength))

        logging.debug(f"Sending data {data}")

        # send msglength and message
        self.socket_to_server.send(msglength)
        self.socket_to_server.send(data)

        logging.debug("Data sent")

    def receive_data(self):
        # result = self.io_stream_server.readline().rstrip("\n")
        data = self.socket_to_server.recv()

        return data

    def session_id(self,value):
        self.session_id = value