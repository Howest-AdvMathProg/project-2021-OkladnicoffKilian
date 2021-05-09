import socket
from time import sleep
import pickle

HEADERSIZE = 128
FORMAT = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostbyname(socket.gethostname()), 5000))
sessid = ""

# s.setblocking(0)
try:
    msg = "login?uname=kilian&fullname=kiokl&email=tets@email.com".encode(FORMAT)
    msglength = len(msg)
    msglength = str(msglength).encode(FORMAT)
    msglength += b' ' * (HEADERSIZE - len(msglength))
    s.send(msglength)
    s.send(msg)
    msglength = int(s.recv(HEADERSIZE).decode(FORMAT))
    data = s.recv(msglength).decode(FORMAT)
    sessid = data

    msg = f"get_confirmed?session_id={sessid}".encode(FORMAT)
    msglength = len(msg)
    msglength = str(msglength).encode(FORMAT)
    msglength += b' ' * (HEADERSIZE - len(msglength))
    s.send(msglength)
    s.send(msg)
    msglength = int(s.recv(HEADERSIZE).decode(FORMAT))
    data = s.recv(msglength).decode(FORMAT)

    obj = pickle.loads(eval(data))
    print(obj)
    sleep(10)

except KeyboardInterrupt:
    s.close()
    exit()
except Exception as e:
    s.close()
    raise e
