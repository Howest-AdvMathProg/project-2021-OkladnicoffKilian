import socket
import json
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 5000))

s.send(json.dumps({"username": "test", "fullname": "testfullname", "email": "testemail"}).encode('ascii'))

print(s.recv(1024).decode('ascii'))

count = 0

while count < 10:
    sleep(1)

s.close()