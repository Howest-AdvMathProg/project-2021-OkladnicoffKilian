import socket
from time import sleep
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import io
from PIL import Image

HEADERSIZE = 128
FORMAT = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostbyname(socket.gethostname()), 5000))
sessid = ""

def login():
    msg = "login?uname=kilian&fullname=kiokl&email=tets@email.com".encode(FORMAT)
    msglength = len(msg)
    msglength = str(msglength).encode(FORMAT)
    msglength += b' ' * (HEADERSIZE - len(msglength))
    s.send(msglength)
    s.send(msg)
    msglength = int(s.recv(HEADERSIZE).decode(FORMAT))
    data = s.recv(msglength).decode(FORMAT)
    return data

def confirmed():
    sessid = login()
    msg = f"get_confirmed?session_id={sessid}".encode(FORMAT)
    msglength = len(msg)
    msglength = str(msglength).encode(FORMAT)
    msglength += b' ' * (HEADERSIZE - len(msglength))
    s.send(msglength)
    s.send(msg)
    msglength = int(s.recv(HEADERSIZE).decode(FORMAT))
    data = s.recv(msglength).decode(FORMAT)
    obj = pickle.loads(eval(data))
    return obj

def byname():
    msg = f"get_kepler_name?name=Kepler-227&session_id={sessid}".encode(FORMAT)
    msglength = len(msg)
    msglength = str(msglength).encode(FORMAT)
    msglength += b' ' * (HEADERSIZE - len(msglength))
    s.send(msglength)
    s.send(msg)
    msglength = int(s.recv(HEADERSIZE).decode(FORMAT))
    data = s.recv(msglength).decode(FORMAT)
    obj = pickle.loads(eval(data))
    return obj

def logout():
    msg = f"logout?session_id={sessid}".encode(FORMAT)
    msglength = len(msg)
    msglength = str(msglength).encode(FORMAT)
    msglength += b' ' * (HEADERSIZE - len(msglength))
    s.send(msglength)
    s.send(msg)
    msglength = int(s.recv(HEADERSIZE).decode(FORMAT))
    data = s.recv(msglength).decode(FORMAT)
    return data

def get_score():
    msg = f"get_koi_score?score=0.5&session_id={sessid}&operand=gt".encode(FORMAT)
    msglength = len(msg)
    msglength = str(msglength).encode(FORMAT)
    msglength += b' ' * (HEADERSIZE - len(msglength))
    s.send(msglength)
    s.send(msg)
    msglength = int(s.recv(HEADERSIZE).decode(FORMAT))
    data = s.recv(msglength).decode(FORMAT)
    obj = pickle.loads(eval(data))
    return obj

def get_countplot():
    msg = f"countplot?session_id={sessid}".encode(FORMAT)
    msglength = len(msg)
    msglength = str(msglength).encode(FORMAT)
    msglength += b' ' * (HEADERSIZE - len(msglength))
    s.send(msglength)
    s.send(msg)
    msglength = int(s.recv(HEADERSIZE).decode(FORMAT))
    received = s.recv(msglength).decode(FORMAT)
    data = b''.join(eval(received))
    img = Image.open(io.BytesIO(data))
    return img

try:
    sessid = login()
    img = get_countplot()
    img.show()
    sleep(10)
    
except KeyboardInterrupt:
    s.close()
    exit()
except Exception as e:
    s.close()
    raise e
