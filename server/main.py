from util.server import Server
import logging
import threading
from time import sleep
import pandas as pd
import pickle
from os import path
import uuid


class Commands:
    logged_in = {}

    def __init__(self):
        self.dataset = pd.read_csv(path.join(path.dirname(__file__), "data/kepler.csv"))
    
    def get_confirmed(self):
        return pickle.dumps(self.dataset[self.dataset['koi_disposition'] == 'CONFIRMED'])

    def check_login(self, session_id):
        if session_id in self.logged_in.keys():
            return True
        return False

    def login(self, uname, fullname, email):
        sessid = uuid.uuid4()
        self.logged_in[str(sessid)] = dict(username = uname, fullname = fullname, email = email)
        return sessid


logging.basicConfig(level=logging.DEBUG, format="%(levelname)s --> %(msg)s")
threading.Thread(target=Server, args=(Commands,), daemon=True).start()

try:
    while True:
        sleep(10)
except KeyboardInterrupt:
    exit()
except Exception as e:
    logging.error(e)