import logging

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

class Logger:
    def __init__(self, name):
        self.__logger = logging.Logger(name=name)
        self.__init_logger()

    def __init_logger(self):
        self.__logger.setLevel(logging.getLogger().getEffectiveLevel())
        sh = logging.StreamHandler()
        formatting = logging.Formatter("[%(asctime)s] %(name)s:%(levelname)s [%(msg)s]")
        sh.setFormatter(formatting)
        self.__logger.addHandler(sh)
    
    def log(self, level, msg):
        self.__logger.log(level, msg)
        if level >= logging.CRITICAL:
            raise Exception(f"{logging.getLevelName(level)}: {msg}")