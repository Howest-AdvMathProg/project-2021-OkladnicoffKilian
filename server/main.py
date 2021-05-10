from os import path
from tkinter import *
from time import sleep
from util.server import Server
from util.interface import Interface
import matplotlib.pyplot as plt
import util.logger as logger
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import operator
import threading
import logging
import pickle
import uuid
import os
mpl.use('Agg')

#decorator to keep track of amount of function calls per endpoint
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
    
    class Endpoints:
        endpoints = {}

        @classmethod
        def route(cls, route):
            def wrapper(func):
                cls.endpoints[route] = func
            return wrapper

    def __init__(self, socket):
        #read in dataset
        self.dataset = pd.read_csv(path.join(path.dirname(__file__), "data/kepler.csv"))
        self.socket = socket
    
    @staticmethod
    def get_endpoint_counts():
        return {k: v.counter for k,v in Commands.Endpoints.endpoints.items()}

    #return all koi object with a confirmed disposition
    @Endpoints.route("confirmed")
    @count_function
    def get_confirmed(self):
        return pickle.dumps(self.dataset[self.dataset['koi_disposition'] == 'CONFIRMED'])
    
    #get koi objects by search query on the name. May be incomplete name
    @Endpoints.route("kepler_name")
    @count_function
    def get_kepler_name(self, name):
        return pickle.dumps(self.dataset[self.dataset['kepler_name'].str.contains(name, na=False, regex=False)])


    #login the user and send back the session id
    @Endpoints.route("login")
    @count_function
    def login(self, uname, fullname, email):
        sessid = str(uuid.uuid4())
        self.logged_in[sessid] = dict(username = uname, fullname = fullname, email = email, socket=self.socket)
        return sessid

    #log the user out, and remove the session from logged in
    @Endpoints.route("logout")
    @count_function
    def logout(self, session_id):
        if session_id in self.logged_in.keys():
            self.logged_in.pop(session_id)
            return 200
        return 404
    
    #filter by koi score
    @Endpoints.route("koi_score")
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
    @Endpoints.route("countplot")
    @count_function
    def countplot(self):

        #generate a graph, and save as a temporary image
        temp_id = uuid.uuid4()
        dirpath = path.dirname(__file__) + f"/temp"
        fp = dirpath + f"/{temp_id}.png"
        
        dataset = self.dataset.copy()
        dataset['koi_disposition'].dropna(axis=0, inplace=True)
        sns.countplot(data=dataset, x='koi_disposition')
        if not path.exists(dirpath):
            os.mkdir(dirpath)
        del dataset
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
    @Endpoints.route("column_names")
    @count_function
    def get_columns(self):
        return list(self.dataset.columns)

    #plot 2 columns in a scatterplot to analyze correlation
    @Endpoints.route("scatterplot")
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

#test function
def print_req_counts():
    while True:
        print(Commands.get_endpoint_counts())
        sleep(5)

def send_message(guid, msg):
    if guid in Commands.logged_in.keys():
        Commands.logged_in[guid]['socket'].send(msg)

try:
    #main logic for server side
    root = Tk()
    gui = Interface(master=root)
    gui.mainloop()
except KeyboardInterrupt:
    exit()
except Exception as e:
    logging.error(e)