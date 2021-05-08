from util.server import Server
import logging

class Commands:
    @staticmethod
    def get():
        return "hello"

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s --> %(msg)s")
server = Server(command_class=Commands)