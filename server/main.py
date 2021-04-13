from utils import server, interface
import logging
import socket
from time import sleep
import threading

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(msg)s")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 5000))

    while True:
        sleep(5)
except KeyboardInterrupt:
    s.close()
