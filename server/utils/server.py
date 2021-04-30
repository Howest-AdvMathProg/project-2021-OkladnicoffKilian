import socket
import logging 
import threading
import multiprocessing
from utils.logger import Logger

class Server_Connection(threading.Thread):
    def __init__(self, connect_func, sock, addr):
        try:
            self.__class__._logger
        except:
            self.__class__._logger = Logger("ServerConnection")

        self.alive = True
        threading.Thread.__init__(self, daemon=True)
        self.connect_func = connect_func
        self.sock = sock
        self.addr = addr

    def run(self):
        try:
            self.connect_func(self.sock, self.addr)
        except Exception as e:
            self._logger.log(logging.ERROR, "Connection encountered an error")
            self._logger.log(logging.DEBUG, f"Error: {e}")
        finally:
            self.sock.close()
            self._logger.log(logging.INFO, f"Closing connection with {self.addr}")
            self.alive = False

    def is_alive(self):
        return self.alive

class Server():
    active_connections = []

    def __init__(self, conn_func, addr=socket.gethostname(), port=5000, max_clients:int=2):
        try:
            self.__class__._logger
        except:
            self.__class__._logger = Logger("Server")

        self.max_clients = max_clients if isinstance(max_clients, int) else self._logger.log(logging.ERROR, "Expected type int for max_clients")
        self.on_connect = conn_func
        self.addr, self.port = addr, port
        self.init()

    def remove_inactive(self):
        while True:
            for t in self.active_connections:
                if t.is_alive():
                    continue
                self.active_connections.remove(t)
                self._logger.log(logging.DEBUG, f"Active threads: {len(self.active_connections)}")

    def init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.addr, self.port))
        self.sock.listen(5)
        self._logger.log(logging.INFO, f"Server up, listening on {self.addr}:{self.port}...")
        threading.Thread(target=self.remove_inactive).start()
        
        while True:
            self._logger.log(logging.INFO, f"Listening for connections...")
            sock_client, addr = self.sock.accept()
            if len(self.active_connections) >= self.max_clients:
                sock_client.close()
                continue
            
            self._logger.log(logging.INFO, f"Got connection from {addr}")
            conn = Server_Connection(self.on_connect, sock_client, addr)
            self.active_connections.append(conn)
            conn.start()

        self._logger.log(logging.INFO, "Server shutting down...")
        self.sock.close()

    @staticmethod
    def is_socket_closed(sock):
        try:
            sock.setblocking(0)
            data = sock.recv(16, socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False
        except ConnectionResetError:
            return True 
        except Exception as e:
            cls._logger.log(logging.CRITICAL, f"Unexpected exception when checking if a socket is closed: {e}")
            return False
        return False

if __name__ == "__main__":
    from time import sleep
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(msg)s")

    def on_connect(sc, addr):
        try:
            while True:
                logging.log(logging.DEBUG, f"On connect for client {addr}")
                if Server.is_socket_closed(sc):
                    break
                sleep(2)
            logging.log(logging.DEBUG, f"Connection closed for {addr}")
        except Exception as e:
            raise e

    try:
        server = Server(on_connect, max_clients=5)
    except KeyboardInterrupt:
        import sys
        sys.exit()
    except Exception as e:
        raise e