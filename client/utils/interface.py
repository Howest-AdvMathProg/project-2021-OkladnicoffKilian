from tkinter import *
from tkinter import ttk
import logging
import re
import json
from .client import Client

class Interface(Frame):
    def __init__(self, master=None):
        # set variables
        Frame.__init__(self, master)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.window_closed)
        self.client = Client(5000)

        self.labels = []
        self.entries = []
        self.buttons = []

        self.pack(fill=BOTH, expand=1)

        # call login screen
        self.login_window()

    # login window
    def login_window(self):
        self.master.title("Login")

        # full name
        label = Label(self, text="Full name")
        label.grid(row=0)
        self.labels.append(label)
        self.entry_name = Entry(self, width=40)
        self.entry_name.grid(row=0, column=1, sticky=E+W, pady=(5,5))
        self.entries.append(self.entry_name)
        # nickname
        label = Label(self, text="Nickname")
        label.grid(row=1)
        self.labels.append(label)
        self.entry_nickname = Entry(self, width=40)
        self.entry_nickname.grid(row=1, column=1, sticky=E+W, pady=(5,5))
        self.entries.append(self.entry_nickname)
        # email
        label = Label(self, text="Email")
        label.grid(row=2)
        self.labels.append(label)
        self.entry_email = Entry(self, width=40)
        self.entry_email.grid(row=2, column=1, sticky=E+W, pady=(5,5))
        self.entries.append(self.entry_email)
        # login error display
        self.login_error = StringVar()
        label = Label(self, textvariable=self.login_error)
        label.grid(row=3,column=1,pady=(5,5))
        self.labels.append(label)
        # connect
        self.login_button = Button(self, text="Login", command=self.login)
        self.login_button.grid(row=4, columnspan=3, pady=(5,5), padx=(5,5), sticky=N+S+E+W)
        self.buttons.append(self.login_button)

        # grid config
        Grid.rowconfigure(self, 4, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

    def login(self):
        # validate inputs
        if self.entry_name.get():
            if self.entry_nickname.get():
                if re.match('([A-Za-z0-9.!#$%&*+\-/=?^_`{|}~]+@[A-Za-z0-9\-\.]+)', self.entry_email.get()):
                    logging.info("Login values valid")

                    # create socket and connect
                    self.client.connect()

                    # send user login data
                    data = {"fullname": self.entry_name.get(), "username": self.entry_nickname.get(), "email": self.entry_email.get()}
                    self.client.send_data(json.dumps(data))

                    # receive user id
                    # if self.client.receive_data():
                        # call main menu
                    # load new window
                    self.reset_window()
                    self.main_menu()

                else:
                    logging.error("Invalid email")
                    self.login_error.set("Invalid email address")
            else:
                logging.error("Invalid nickname: nickname cannot be empty")
                self.login_error.set("Nickname cannot be empty")
        else:
            logging.error("Invalid name: full name cannot be empty")
            self.login_error.set("Full name cannot be empty")

    # main menu
    def main_menu(self):
        # # create menu tabs
        # menu = Menu(self.master)
        # self.master.config(menu=menu)

        # # create user tab
        # user = Menu(menu)
        # user.add_command(label="Logout", command=self.window_closed)
        # menu.add_cascade(label="User", menu=user)   

        # create parent for tabs
        tab_control = ttk.Notebook(self.master)

        # create tab for each function
        for i in range(0, 5):
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=f"Tab {i}")

        # visualise tabs
        tab_control.pack(expand=1, fill="both")

    # method called when window is closed
    def window_closed(self):
        # close connection
        self.client.disconnect()

        # close window
        self.master.destroy()
        exit()

    # reset window contents
    def reset_window(self):
        self.master.title("Kepler")
        for item in self.labels:
            item.destroy()
        for item in self.entries:
            item.destroy()
        for item in self.buttons:
            item.destroy()

        self.labels = []
        self.entries = []
        self.buttons = []