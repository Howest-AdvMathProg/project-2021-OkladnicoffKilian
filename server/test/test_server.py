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
    msg = f"confirmed?session_id={sessid}".encode(FORMAT)
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
    msg = f"kepler_name?name=Kepler-227&session_id={sessid}".encode(FORMAT)
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
    msg = f"koi_score?score=0.5&session_id={sessid}&operand=gt".encode(FORMAT)
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
    print(data)
    img = Image.open(io.BytesIO(data))
    print(img)
    return img

def get_scatterplot(x=None,y=None):
    if x and y:
        msg = f"scatterplot?session_id={sessid}&x={x}&y={y}".encode(FORMAT)
    else:
        msg = f"scatterplot?session_id={sessid}".encode(FORMAT)
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

def get_columns():
    msg = f"column_names?session_id={sessid}".encode(FORMAT)
    msglength = len(msg)
    msglength = str(msglength).encode(FORMAT)
    msglength += b' ' * (HEADERSIZE - len(msglength))
    s.send(msglength)
    s.send(msg)
    msglength = int(s.recv(HEADERSIZE).decode(FORMAT))
    data = s.recv(msglength).decode(FORMAT)
    return data

try:
    sessid = login()
    data = confirmed()
    print(data)
    data = byname()
    print(data)
    data = get_score()
    print(data)
    data = get_countplot()
    data.show()
    data = get_scatterplot()
    data.show()
    data = get_columns()
    print(data)
    print(logout())
    sleep(10)
    
except KeyboardInterrupt:
    s.close()
    exit()
except Exception as e:
    s.close()
    raise e
