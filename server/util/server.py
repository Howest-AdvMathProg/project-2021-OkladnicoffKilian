import socket
import util.logger as logger
import threading
import logging
from time import sleep

class Server:
    class ClientHandler(threading.Thread):
        active_connections = []

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
            self.commands = command_class()
            self.sessid = None
            self.connected = True

        def receive(self):
            msgsize = self.s.recv(self.HEADERSIZE).decode(self.FORMAT)
            if msgsize:
                msgsize = int(msgsize)
                data = self.s.recv(msgsize).decode(self.FORMAT)
                self.logger.log(logger.DEBUG, f"Received data from {self.addr}: {data}")
                
                data = data.split("?")
                if len(data) > 1:
                    data[1] = {x.split("=")[0]: x.split("=")[1] for x in data[1].split("&")}
                return data

        def send(self, data):
            if type(data) != str:
                data = str(data)
            data = bytes(data, self.FORMAT)
            size = bytes(str(len(data)), self.FORMAT)
            size = size + b" "*(self.HEADERSIZE - len(size))
            self.s.send(size)
            self.s.send(data)

        def check_closed(self):
            while True:
                try:
                    if len(self.s.recv(16, socket.MSG_PEEK)) == 0:
                        self.logger.log(logger.WARNING, "Client disconnected")
                        break
                except ConnectionError:
                    break
            self.active_connections.remove(self)
            self.connected = False

        def run(self):
            threading.Thread(target=self.check_closed, daemon=True).start()
            while self.connected:
                data = self.receive()
                if data:
                    try:
                        if data[0] != 'login':
                            try:
                                if not self.commands.check_login(data[1]['session_id']):
                                    raise TypeError("Access denied")
                                del data[1]['session_id']
                            except Exception as e:
                                self.logger.log(logger.DEBUG, e)
                                raise TypeError('missing session id')
                        else:
                            if self.sessid != None: 
                                if self.sessid in self.commands.logged_in.keys():
                                    self.send("Already logged in, please log out first")
                                    continue
                        retval = getattr(self.commands, data[0])(**data[1]) if len(data) > 1 else getattr(self.commands, data[0])()
                        if data[0] == 'login':
                            self.sessid = retval
                        self.send(retval)
                    except NotImplementedError:
                        self.send("Command not found")
                    except TypeError as e:
                        self.logger.log(logger.DEBUG, e)
                        self.send("Could not process request")
                    except Exception as e:
                        self.logger.log(logger.ERROR, str(type(e)) + " | " + str(e))
                        self.connected = False
            try:
                try:
                    self.commands.logout(self.sessid)
                except Exception as e:
                    self.logger.log(logger.DEBUG, e)
                self.s.close()
            except:
                pass
            self.logger.log(logger.INFO, "Closing socket...")

    def __init__(self, command_class, host=socket.gethostbyname(socket.gethostname()), port=5000, max_clients=5):
        try:
            self.__class__.logger
        except:
            self.__class__.logger = logger.Logger("Server")

        self.hostname = host
        self.port = port
        self.command_class = command_class
        self.max_clients = max_clients
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.start()

    def log_active(self):
        while True:
            self.logger.log(logger.DEBUG, f"Active connections {len(self.ClientHandler.active_connections)}")
            sleep(240)

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