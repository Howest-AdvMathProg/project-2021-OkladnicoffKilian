from utils import server, interface
import logging
import socket
import json

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(msg)s")

def on_connect(self, sc, addr):
    try:
        io_stream = sc.makefile(mode='rw')
        while True:
            data = io_stream.readline().rstrip()
            if self.is_socket_closed(self, sc):
                break
            if len(data) == 0:
                continue
            
            self.log(logging.INFO, f"Received {data}")
        self.log(logging.INFO, f"Disconnecting {addr}")
    except KeyboardInterrupt:
        import sys
        sys.exit()
    except Exception as e:
        raise e

if __name__ == "__main__":
    s = server.Server(on_connect)