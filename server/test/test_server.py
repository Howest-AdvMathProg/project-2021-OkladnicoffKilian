import socket
from time import sleep

HEADERSIZE = 128
FORMAT = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostbyname(socket.gethostname()), 5000))

s.setblocking(0)
try:
    msg = "test".encode(FORMAT)
    msglength = len(msg)
    msglength = str(msglength).encode(FORMAT)
    msglength += b' ' * (HEADERSIZE - len(msglength))
    s.send(msglength)
    s.send(msg)
    sleep(10)

except KeyboardInterrupt:
    s.close()
    exit()
except Exception as e:
    s.close()
    raise e
