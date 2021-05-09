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
import util.logger as logger


def count_function(func):
    def wrapper(*args, **kwargs):
        wrapper.counter += 1
        return func(*args, **kwargs)
    wrapper.counter = 0
    return wrapper

#class containing all endpoints and command related code
class Commands:
    logged_in = {}

    #init logger
    logger = logger.Logger("Commands", file=True, loglevel=logging.INFO, fileformatter=logging.Formatter("[%(asctime)s] %(user)s(%(uname)s) requested %(msg)s"))

    def __init__(self):
        #read in dataset
        self.dataset = pd.read_csv(path.join(path.dirname(__file__), "data/kepler.csv"))
    
    #return all koi object with a confirmed disposition
    def get_confirmed(self):
        return pickle.dumps(self.dataset[self.dataset['koi_disposition'] == 'CONFIRMED'])
    
    #get koi objects by search query on the name. May be incomplete name
    @count_function
    def get_kepler_name(self, name):
        return pickle.dumps(self.dataset[self.dataset['kepler_name'].str.contains(name, na=False, regex=False)])

    #function to check if the user is a logged in user. Serves as an extra check
    def check_login(self, session_id):
        if session_id in self.logged_in.keys():
            return True
        return False

    #login the user and send back the session id
    @count_function
    def login(self, uname, fullname, email):
        sessid = str(uuid.uuid4())
        self.logged_in[sessid] = dict(username = uname, fullname = fullname, email = email)
        return sessid

    #log the user out, and remove the session from logged in
    @count_function
    def logout(self, session_id):
        if session_id in self.logged_in.keys():
            self.logged_in.pop(session_id)
            return 200
        return 404
    
    #filter by koi score
    @count_function
    def get_koi_score(self, score, operand='lt'):
        try:
            #operands to be used
            ops = {
                'lt': operator.lt,
                'le': operator.le,
                'eq': operator.eq,
                'ge': operator.ge,
                'gt': operator.gt
            }
            score = float(score)

            #if score out of range, raise error
            if score > 1 or score < 0:
                raise ValueError()
            #return the filtered data as a pickled pandas dataframe
            return pickle.dumps(self.dataset[ops[operand.lower()](self.dataset['koi_score'], score)])
        except Exception as e:
            logging.error(e)
            return 400 #will mainly trigger if operand is not defined

    #get a countplot of the koi dispositions
    @count_function
    def countplot(self):

        #generate a graph, and save as a temporary image
        temp_id = uuid.uuid4()
        dirpath = path.dirname(__file__) + f"/temp"
        fp = dirpath + f"/{temp_id}.png"
        
        sns.countplot(data=self.dataset['koi_disposition'].dropna(axis=0, inplace=False), x="koi_disposition")
        if not path.exists(dirpath):
            os.mkdir(dirpath)
        
        #reset pyplot and save the graph
        plt.savefig(fp)
        plt.close('all')

        #keep trying to open the image, may cause errors because pyplot is still saving it
        while True:
            try:
                with open(fp, 'rb') as f:
                    data = f.readlines()
                    f.close()
                if data: #once the image is read, exit loop
                    break
            except:
                pass

        #try to remove the temp image to save memory on disk
        while True:
            try:
                os.remove(fp)
                print(os.path.exists(fp))
                if not path.exists(fp):
                    break
            except Exception as e:
                print(e)
        #return image bytes
        return data

    #get all possible column filters for scatterplot
    @count_function
    def get_columns(self):
        return list(self.dataset.columns)

    #plot 2 columns in a scatterplot to analyze correlation
    @count_function
    def scatterplot(self, x='koi_teq', y='koi_srad'):

        #same method of working as countplot
        temp_id = uuid.uuid4()
        dirpath = path.dirname(__file__) + f"/temp"
        fp = dirpath + f"/{temp_id}.png"
        
        dataset = self.dataset[[x, y]].dropna(axis=0, inplace=False)
        plt.scatter(dataset[x], dataset[y])
        plt.xlabel(x)
        plt.ylabel(y)
        if not path.exists(dirpath):
            os.mkdir(dirpath)
        
        plt.savefig(fp)
        plt.close('all')

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
logging.getLogger('matplotlib.font_manager').setLevel(logging.CRITICAL) #ignore matplotlib messages concerning fonts
threading.Thread(target=Server, args=(Commands,), daemon=True).start() #start the server in a daemon. This makes the programm quittable with ^C, etc.

try:
    #main logic for server side
    while True:
        sleep(0.1)
except KeyboardInterrupt:
    exit()
except Exception as e:
    logging.error(e)