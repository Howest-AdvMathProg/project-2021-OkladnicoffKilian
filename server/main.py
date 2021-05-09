from util.server import Server
import logging
import threading
from time import sleep

class Commands:
    @staticmethod
    def get(message):
        return message

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s --> %(msg)s")
threading.Thread(target=Server, args=(Commands,), daemon=True).start()

try:
    while True:
        sleep(10)
except KeyboardInterrupt:
    exit()
except Exception as e:
    logging.error(e)