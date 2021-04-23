from tkinter import Tk
import logging
import socket

from utils.interface import Interface

# set logging level
logging.basicConfig(level=logging.INFO)

root = Tk()
app = Interface(root)
root.mainloop()