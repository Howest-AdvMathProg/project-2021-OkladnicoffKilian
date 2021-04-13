import socket
import logging 
import threading
import multiprocessing

class Server:
    logger = logging.Logger(name="Server")

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
        self.sock.settimeout(30)
        self.log(logging.INFO, f"Server up, listening on {self.addr}:{self.port}...")
        self.running = True
        self.active_threads = []

        while self.running:
            if len(self.active_threads) < self.max_clients:
                self.logger.debug("Waiting for connections...")
                sock_client, client_addr = self.sock.accept()    
                [self.active_threads.remove(i) for i in self.active_threads if i.isAlive == False]
                t = threading.Thread(target=self.on_connect, args=(self, sock_client))
                t.daemon = True
                t.start()
                self.active_threads.append(t)
                self.logger.info(f"Active threads: {len(self.active_threads)}")

        self.log(logging.INFO, "Server shutting down...")
        self.sock.close()

    def init_logger(self):
        self.logger.setLevel(logging.getLogger().getEffectiveLevel())
        formatter = logging.Formatter("[%(asctime)s] %(name)s:%(levelname)s [%(msg)s]")
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

if __name__ == "__main__":
    from time import sleep
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(msg)s")

    def on_connect(self, sc):
        i = 0
        while True:
            if i < 1:
                print("on connect executed")
                i += 1
            sleep(5)
            
    try:
        server = Server(on_connect, max_clients=5)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        raise e