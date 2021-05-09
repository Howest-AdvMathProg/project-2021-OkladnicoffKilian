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

    #initializes the logger. This also sets the cutom level and enables logging to file instead of terminal if the options are passed
    def __init_logger(self):
        #set the log level to the given level, if not specified use root level
        self.__logger.setLevel(logging.getLogger().getEffectiveLevel()) if self.loglevel == None else self.__logger.setLevel(self.loglevel)
        
        #set formatting
        formatting = logging.Formatter("[%(asctime)s] %(name)s:%(levelname)s [%(msg)s]")
        
        #if this is enabled log wil use a file instead of console
        if self.file == True:
            dirpath = path.join(path.dirname(__file__), path.relpath(f"../logs"))
            if not path.exists(dirpath): #create logs directory if not present
                os.mkdir(dirpath)
            
            fh = logging.FileHandler(dirpath + f"/{self.name}.log", 'a')
            
            #if custom file formatting was specified, use this. Else use the default formatting
            fmt = formatting if self.fileformatter == None else self.fileformatter
            fh.setFormatter(fmt)

            #add the handler to enable it
            self.__logger.addHandler(fh)
        else:
            #create a streamhandler for output
            sh = logging.StreamHandler()
            sh.setFormatter(formatting)
            self.__logger.addHandler(sh)
    
    #this function will log the message at given level, and raise an error if it exceeds critical level
    def log(self, level, msg, extra=None):
        self.__logger.log(level, msg) if extra == None else self.__logger.log(level, msg, extra=extra)
        if level >= logging.CRITICAL:
            raise Exception(f"{logging.getLevelName(level)}: {msg}")