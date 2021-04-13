import threading

class Thread(threading.Thread):
    instances = set()
    lock = None

    def __init__(self, name, func, *args):
        super().__init__(name=name, target=func, args=args)
        self.name = name

        if self.lock == None:
            self.lock = threading.Lock()

        self.instances.add(self)

    def start(self):
        super().init

    def __del__(self):
        self.instances.remove(self)