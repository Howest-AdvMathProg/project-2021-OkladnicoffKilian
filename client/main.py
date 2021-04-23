from tkinter import Tk
import logging
import socket

from utils.interface import Interface

# set logging level
logging.basicConfig(level=logging.DEBUG)

root = Tk()
app = Interface(root)
root.mainloop()