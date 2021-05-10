import logging
import socket
from tkinter import messagebox

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

    def disconnect(self):
        # check for session id --> if there notify server of disconnect
        if self.session_id != None:
            data = f"logout?"
            self.send_data(data)
            response = self.receive_data()
            if response == "200":
                logging.info("Server disconnected")
            else:
                logging.warning("Server encountered an error")

        self.socket_to_server.close()
        logging.info("Client closed")

    def send_data(self, data):
        # if client has a sessionid it needs to be send aswell
        if self.session_id != None:
            data += f"&session_id={self.session_id}" if data[-1]!="?" else f"session_id={self.session_id}"
            
        data = data.encode(encoding_format)

        try:
            # calculate msg length
            msglength = len(data)
            msglength = str(msglength).encode(encoding_format)
            msglength += b' ' * (headersize - len(msglength))

            logging.debug(f"Sending data {data}")

            # send msglength and message
            self.socket_to_server.send(msglength)
            self.socket_to_server.send(data)

            logging.debug("Data sent")
        except Exception as ex:
            logging.error(str(ex))
            messagebox.showinfo("Connection error", "Something went wrong...")
            exit()

    def receive_data(self):
        try:
            msglength = int(self.socket_to_server.recv(headersize).decode(encoding_format))

            if msglength:
                data = self.socket_to_server.recv(msglength).decode(encoding_format)

            return data
        except Exception as ex:
            logging.error(str(ex))
            messagebox.showinfo("Connection error", "Something went wrong...")
            exit()

    def session_id(self,value):
        self.session_id = value