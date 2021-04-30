from utils import server, interface
import logging
import socket
import json
import uuid

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(msg)s")

class User:
    def __init__(self, uname, fullname, email, sock):
        self.sock = sock
        self.username = uname
        self.fullname = fullname
        self.email = email
        self.session_id = uuid.uuid4()
    
def on_connect(self, sc, addr):
    try:
        creds = sc.recv(1024).decode('ascii')
        creds = json.loads(creds)
        u = User(creds['username'], creds['fullname'], creds['email'], sc)
        self.log(logging.DEBUG, f"Created user with id {u.session_id}")
        sc.send(json.dumps({"sessionId": u.session_id.__str__()}).encode('ascii'))

    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    s = server.Server(on_connect)