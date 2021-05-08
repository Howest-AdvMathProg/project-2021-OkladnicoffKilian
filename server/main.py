from util.server import Server
import logging

class Commands:
    @staticmethod
    def get(message):
        return message

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s --> %(msg)s")
server = Server(command_class=Commands)