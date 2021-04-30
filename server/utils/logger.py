import logging

class Logger:
    def __init__(self, name):
        self.logger = logging.Logger(name)
        self.init_logger()

    def log(self, level, msg):
        self.logger.log(level, msg)
        if level >= logging.ERROR:
            raise Exception(msg)

    def init_logger(self):
        # self.logger.setLevel(logging.getLogger("root").getEffectiveLevel())
        formatter = logging.Formatter("[%(asctime)s] %(name)s:%(levelname)s [%(msg)s]")
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)