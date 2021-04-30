import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 5000))

s.send(json.dumps({"username": "test", "fullname": "testfullname", "email": "testemail"}).encode('ascii'))

print(s.recv(1024).decode('ascii'))

s.close()