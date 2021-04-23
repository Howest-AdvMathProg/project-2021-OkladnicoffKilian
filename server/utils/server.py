import socket
import logging 
import threading
import multiprocessing

class Server:
    logger = logging.Logger(name="Server")
    active_connections = []

    def __init__(self, conn_func, addr=socket.gethostname(), port=5000, max_clients:int=2):
        self.init_logger()
        self.max_clients = max_clients if isinstance(max_clients, int) else self.log(logging.ERROR, "Expected type int for max_clients")
        self.on_connect = conn_func
        self.addr, self.port = addr, port
        self.init()

    def log(self, level, msg):
        self.logger.log(level=level, msg=msg)
        if level >= logging.ERROR:
            raise Exception(msg)

    def init(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.addr, self.port))
        self.sock.listen(5)
        self.log(logging.INFO, f"Server up, listening on {self.addr}:{self.port}...")

        while True:
            self.log(logging.INFO, f"Listening for connections...")
            sock_client, addr = self.sock.accept()
            if len(self.active_connections) >= self.max_clients:
                sock_client.close()
                continue
            
            self.log(logging.INFO, f"Got connection from {addr}")
            t = threading.Thread(target=self.on_connect, args=(self, sock_client, addr))
            t.daemon = True
            self.active_connections.append(t)
            t.start()
        self.log(logging.INFO, "Server shutting down...")
        self.sock.close()

    @staticmethod
    def is_socket_closed(server, sock: socket.socket) -> bool:
        try:
            sock.setblocking(0)
            data = sock.recv(16)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False
        except ConnectionResetError:
            return True 
        except Exception as e:
            server.log(logging.CRITICAL, f"Unexpected exception when checking if a socket is closed: {e}")
            return False
        return False

    def init_logger(self):
        self.logger.setLevel(logging.getLogger().getEffectiveLevel())
        formatter = logging.Formatter("[%(asctime)s] %(name)s:%(levelname)s [%(msg)s]")
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

if __name__ == "__main__":
    from time import sleep
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(msg)s")

    def on_connect(self, sc, addr):
        try:
            while True:
                self.log(logging.DEBUG, f"On connect for client {addr}")
                if Server.is_socket_closed(self, sc):
                    break
                sleep(2)
            self.log(logging.DEBUG, f"Connection closed for {addr}")
        except Exception as e:
            raise e

    try:
        server = Server(on_connect, max_clients=5)
    except KeyboardInterrupt:
        import sys
        sys.exit()
    except Exception as e:
        raise e