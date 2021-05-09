from util.server import Server
import logging
import threading
from time import sleep
import pandas as pd
import pickle
from os import path
import uuid
import operator
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os


class Commands:
    logged_in = {}

    def __init__(self):
        self.dataset = pd.read_csv(path.join(path.dirname(__file__), "data/kepler.csv"))
    
    def get_confirmed(self):
        return pickle.dumps(self.dataset[self.dataset['koi_disposition'] == 'CONFIRMED'])
    
    def get_kepler_name(self, name):
        return pickle.dumps(self.dataset[self.dataset['kepler_name'].str.contains(name, na=False, regex=False)])

    def check_login(self, session_id):
        if session_id in self.logged_in.keys():
            return True
        return False

    def login(self, uname, fullname, email):
        sessid = str(uuid.uuid4())
        self.logged_in[sessid] = dict(username = uname, fullname = fullname, email = email)
        return sessid

    def logout(self, session_id):
        if session_id in self.logged_in.keys():
            self.logged_in.pop(session_id)
            return 200
        return 404
    
    def get_koi_score(self, score, operand='lt'):
        try:
            ops = {
                'lt': operator.lt,
                'le': operator.le,
                'eq': operator.eq,
                'ge': operator.ge,
                'gt': operator.gt
            }
            score = float(score)
            if score > 1 or score < 0:
                raise ValueError()
            return pickle.dumps(self.dataset[ops[operand.lower()](self.dataset['koi_score'], score)])
        except Exception as e:
            logging.error(e)
            return 400 #will mainly trigger if operand is not defined

    def countplot(self):
        temp_id = uuid.uuid4()
        dirpath = path.dirname(__file__) + f"/temp"
        fp = dirpath + f"/{temp_id}.png"
        
        sns.countplot(data=self.dataset.dropna(axis=1, inplace=False), x="koi_disposition")
        if not path.exists(dirpath):
            os.mkdir(dirpath)
        
        plt.savefig(fp)

        while True:
            try:
                with open(fp, 'rb') as f:
                    data = f.readlines()
                    f.close()
                if data:
                    break
            except:
                pass

        while True:
            try:
                os.remove(fp)
                print(os.path.exists(fp))
                if not path.exists(fp):
                    break
            except Exception as e:
                print(e)

        return data


logging.basicConfig(level=logging.DEBUG, format="%(name)s:%(levelname)s --> %(msg)s")
logging.getLogger('matplotlib.font_manager').setLevel(logging.CRITICAL)
threading.Thread(target=Server, args=(Commands,), daemon=True).start()

try:
    while True:
        sleep(10)
except KeyboardInterrupt:
    exit()
except Exception as e:
    logging.error(e)