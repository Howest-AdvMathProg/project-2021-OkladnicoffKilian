from utils import server, interface
from utils.logger import Logger
import logging
import socket
import json
import uuid
from time import sleep

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(msg)s")

class User:
    def __init__(self, uname, fullname, email, sock):
        self.sock = sock
        self.username = uname
        self.fullname = fullname
        self.email = email
        self.session_id = uuid.uuid4()
    
class ClientHandler():
    active_users = []

    def __init__(self, user):
        self.user = user
        self.active_users.append(user)

        try:
            self.__class__.functions
        except:
            self.__class__.functions = self.get_functions()
        
        try:
            self.__class__._logger
        except:
            self.__class__._logger = Logger("ClientHandler")

    def mainloop(self):
        self.user.sock.setblocking(0)
        logging.debug(f"active threads: {len(server.Server.active_connections)}")
        try:
            while True:
                if server.Server.is_socket_closed(self.user.sock):
                    break

                # data = self.user.sock.recv(1024)
                # if len(data) > 0:
                #     data = data.decode("ascii")
                
        except Exception as e:
            logging.error(e)
        finally:
            self.active_users.remove(self.user)

    @classmethod
    def get_functions(cls):
        return {k: v for k,v in cls.__dict__.items() if "function_" in k}

    def function_ping():
        return "pong"

def on_connect(sc, addr):
    try:
        creds = sc.recv(1024).decode('ascii')
        creds = json.loads(creds)
        u = User(creds['username'], creds['fullname'], creds['email'], sc)
        logging.log(logging.DEBUG, f"Created user with id {u.session_id}")
        sc.send(json.dumps({"sessionId": u.session_id.__str__()}).encode('ascii'))
        ClientHandler(u).mainloop()
    
    except Exception as e:
        logging.error("Error in connection")
        logging.debug(e)

if __name__ == "__main__":
    s = server.Server(on_connect)