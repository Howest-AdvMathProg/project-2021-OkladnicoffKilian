import logging
from os import path
import os

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

class Logger:
    def __init__(self, name, file=False, loglevel=None, fileformatter=None):
        self.__logger = logging.Logger(name=name)
        self.name = name
        self.file = file
        self.loglevel = loglevel
        self.fileformatter = fileformatter
        self.__init_logger()

    def __init_logger(self):
        self.__logger.setLevel(logging.getLogger().getEffectiveLevel()) if self.loglevel == None else self.__logger.setLevel(self.loglevel)
        sh = logging.StreamHandler()
        formatting = logging.Formatter("[%(asctime)s] %(name)s:%(levelname)s [%(msg)s]")
        if self.file == True:
            dirpath = path.join(path.dirname(__file__), path.relpath(f"../logs"))
            if not path.exists(dirpath):
                os.mkdir(dirpath)
            fh = logging.FileHandler(dirpath + f"/{self.name}.log", 'a')
            fmt = formatting if self.fileformatter == None else self.fileformatter
            fh.setFormatter(fmt)
            self.__logger.addHandler(fh)
        else:
            sh.setFormatter(formatting)
            self.__logger.addHandler(sh)
    
    def log(self, level, msg, extra=None):
        self.__logger.log(level, msg) if extra == None else self.__logger.log(level, msg, extra=extra)
        if level >= logging.CRITICAL:
            raise Exception(f"{logging.getLevelName(level)}: {msg}")