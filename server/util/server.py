import socket
import util.logger as logger
import threading
import logging
from time import sleep

class Server:
    #local handler class for server clients
    class ClientHandler(threading.Thread):
        #keep track of open sockets
        active_connections = []

        HEADERSIZE = 128
        FORMAT = 'utf-8'

        def __init__(self, sock, addr, command_class):
            #start a thread
            super().__init__(None, daemon=True)

            #if the class logger has not been initialized yet, create it
            try:
                self.__class__.logger
            except:
                self.__class__.logger = logger.Logger("ClientHandler")

            self.active_connections.append(self)
            self.s = sock
            self.addr = addr
            self.commands = command_class()
            self.sessid = None
            self.connected = True

        #receive function to receive incoming messages
        def receive(self):
            #first retrieve the size of the following message
            msgsize = self.s.recv(self.HEADERSIZE).decode(self.FORMAT)
            if msgsize:
                msgsize = int(msgsize)

                #once the size has been received, read the data from the buffer
                data = self.s.recv(msgsize).decode(self.FORMAT)
                self.logger.log(logger.DEBUG, f"Received data from {self.addr}: {data}")
                
                #since we work with endpoint?query=value&... format, convert it to an usable object
                data = data.split("?")
                if len(data) > 1:
                    data[1] = {x.split("=")[0]: x.split("=")[1] for x in data[1].split("&")}
                return data

        #method to send data
        def send(self, data):
            #convert data to string if it is of another type
            if type(data) != str:
                data = str(data)
            
            #get the bytes from the data
            data = bytes(data, self.FORMAT)

            #determine the size of the data
            size = bytes(str(len(data)), self.FORMAT)

            #add empty space (=padding) until size reaches the required headersize
            size = size + b" "*(self.HEADERSIZE - len(size))
            
            #send the msg size followed by the data
            self.s.send(size)
            self.s.send(data)

        #method the check every connected socket if it is closed
        def check_closed(self):
            while True:
                try:
                    #socket will send empty data on connection interrupt, catch this empty call
                    if len(self.s.recv(16, socket.MSG_PEEK)) == 0:
                        self.logger.log(logger.WARNING, "Client disconnected")
                        break
                except ConnectionError:
                    break
            
            #when the socket has been closed, remove this object from the class variable
            self.active_connections.remove(self)
            self.connected = False #set connected false to cause an exit in run

        def run(self):
            #start a thread to check socket status
            threading.Thread(target=self.check_closed, daemon=True).start()
            
            #as long as socket is alive, keep running
            while self.connected:
                data = self.receive()
                if data:
                    try:
                        #no need to check for access on login and logout
                        if data[0] not in ['login', 'logout']:
                            try:
                                if not data[1]['session_id'] in self.commands.logged_in.keys():
                                    raise PermissionError("Access denied")
                                del data[1]['session_id']
                            except Exception as e:
                                self.logger.log(logger.DEBUG, e)
                                raise TypeError('missing session id')
                        else: #if the endpoint is login or logout executre this check
                            if self.sessid != None and data[0] != 'logout': #if not trying to log out, double check if session id is still logged in
                                if self.sessid in self.commands.logged_in.keys(): #if session id is still registered send error
                                    self.send(409) # user is already logged in and needs to log out
                                    continue
                        retval = getattr(self.commands, data[0])(**data[1]) if len(data) > 1 else getattr(self.commands, data[0])() #execute the requested endpoint with its parameters
                        print(getattr(self.commands, data[0]).counter)
                        
                        #if the user just logged in, link the session id to this socket
                        if data[0] == 'login':
                            self.sessid = retval
                        try:
                            #log the endpoint calls
                            self.commands.logger.log(logger.INFO, data[0], extra={"user": self.sessid, "uname": next(v['username'] for k,v in self.commands.logged_in.items() if k == self.sessid)})
                        except Exception as e:
                            self.logger.log(logger.DEBUG, e)
                        self.send(retval)
                    except NotImplementedError:
                        self.send(404) # triggers on command not found
                    except PermissionError as e:
                        self.logger.log(logger.DEBUG, e)
                        self.send(401) # happens when user is not logged in, and thus causes an access denied
                    except TypeError as e:
                        self.logger.log(logger.DEBUG, e)
                        self.send(500) # error concerning the given parameters
                    except Exception as e: # any other error that is not expected
                        self.logger.log(logger.ERROR, str(type(e)) + " | " + str(e))
                        self.connected = False
            try: #when the connection is lost, the user will be logged out, and the socker will be closed
                try:
                    self.commands.logout(self.sessid)
                except Exception as e:
                    self.logger.log(logger.DEBUG, e)
                self.s.close()
            except:
                pass
            self.logger.log(logger.INFO, "Closing socket...")

    def __init__(self, command_class, host=socket.gethostbyname(socket.gethostname()), port=5000, max_clients=5):
        try:
            self.__class__.logger
        except:
            self.__class__.logger = logger.Logger("Server")

        self.hostname = host
        self.port = port
        self.command_class = command_class
        self.max_clients = max_clients
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        self.start()

    #simple method to keep logging the amount of connected clients in a developments environment.
    def log_active(self):
        while True:
            self.logger.log(logger.DEBUG, f"Active connections {len(self.ClientHandler.active_connections)}")
            sleep(240)

    #start the server
    def start(self):
        #bind it to the correct port and ip
        self.s.bind((self.hostname, self.port))
        self.s.listen(5)
        self.logger.log(logger.INFO, "Server online, listening for connections...")
        threading.Thread(target=self.log_active, daemon=True).start()

        #main server loop
        while True:
            #when connection is registered, log it and start a clienthandler
            sock_client, addr = self.s.accept()
            self.logger.log(logger.INFO, f"Got connection from {addr}")

            #if a connecting client exceeds the max allowed clients, close the connection
            if len(self.ClientHandler.active_connections) < self.max_clients:
                conn = self.ClientHandler(sock_client, addr, self.command_class).start()
            else:
                sock_client.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s --> %(msg)s")
    server = Server()