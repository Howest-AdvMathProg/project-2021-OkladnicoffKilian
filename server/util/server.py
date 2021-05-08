import socket
import util.logger as logger
import threading
import logging
from time import sleep

class Server:
    class ClientHandler(threading.Thread):
        active_connections = []
        logged_in = {}

        HEADERSIZE = 128
        FORMAT = 'utf-8'

        def __init__(self, sock, addr, command_class):
            super().__init__(None, daemon=True)

            try:
                self.__class__.logger
            except:
                self.__class__.logger = logger.Logger("ClientHandler")

            self.active_connections.append(self)
            self.s = sock
            self.addr = addr
            self.commands = {k:v for k,v in command_class.__dict__.items() if not k.startswith("__")}
            self.connected = True

        def receive(self):
            msgsize = self.s.recv(self.HEADERSIZE).decode(self.FORMAT)
            if msgsize:
                msgsize = int(msgsize)
                data = self.s.recv(msgsize).decode(self.FORMAT)
                self.logger.log(logger.DEBUG, f"Received data from {self.addr}: {data}")
                self.logger.log(logger.DEBUG, f"Available commands = {self.commands}")
                

        def send(self, data):
            data = data.encode(self.FORMAT)
            size = str(len(data)).encode(self.FORMAT)
            size = str(len(data)) + b" "*(self.HEADERSIZE - len(size))
            self.s.send(size)
            self.s.send(data)

        def check_closed(self):
            while True:
                if len(self.s.recv(16, socket.MSG_PEEK)) == 0:
                    self.logger.log(logger.WARNING, "Client disconnected")
                    break
            self.active_connections.remove(self)
            self.connected = False

        def run(self):
            threading.Thread(target=self.check_closed, daemon=True).start()
            while self.connected:
                self.receive()
            self.logger.log(logger.INFO, "Closing socket...")

    def __init__(self, command_class, host=socket.gethostbyname(socket.gethostname()), port=5000, max_clients=5):
        try:
            self.__class__._logger
        except:
            self.__class__.logger = logger.Logger("Server")

        self.hostname = host
        self.port = port
        self.command_class = command_class
        self.max_clients = max_clients
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()

    def log_active(self):
        while True:
            self.logger.log(logger.DEBUG, f"Active connections {len(self.ClientHandler.active_connections)}")
            sleep(120)

    def start(self):
        self.s.bind((self.hostname, self.port))
        self.s.listen(5)
        self.logger.log(logger.INFO, "Server online, listening for connections...")
        threading.Thread(target=self.log_active, daemon=True).start()

        while True:
            sock_client, addr = self.s.accept()
            self.logger.log(logger.INFO, f"Got connection from {addr}")
            if len(self.ClientHandler.active_connections) < self.max_clients:
                conn = self.ClientHandler(sock_client, addr, self.command_class).start()
            else:
                sock_client.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s --> %(msg)s")
    server = Server()