from utils import server, interface
import logging
import socket
from time import sleep
import threading

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(msg)s")
n_clients = 6

def connect(sock):
    try:
        sock.connect((socket.gethostname(), 5000))
        counter = 0
        max_count = 3
        while counter < max_count:
            sleep(5)
            counter += 1
        logging.info(f"Closing connection for {sock}")
    except Exception as e:
        logging.error(e.__str__())
        
try:
    sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in range(n_clients)]
    threads = [threading.Thread(target=connect, args=(s,)) for s in sockets]
    [t.start() for t in threads]
except KeyboardInterrupt:
    s.close()
