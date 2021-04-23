from tkinter import *
import logging
import re
from .client import Client

class Interface(Frame):
    def __init__(self, master=None):
        # set variables
        Frame.__init__(self, master)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.window_closed)
        self.client = Client(5000)

        # call login screen
        self.login_window()

    # login window
    def login_window(self):
        self.master.title("Login")

        self.pack(fill=BOTH, expand=1)

        # content
        # full name
        Label(self, text="Full name").grid(row=0)
        self.entry_name = Entry(self, width=40)
        self.entry_name.grid(row=0, column=1, sticky=E+W, pady=(5,5))
        # nickname
        Label(self, text="Nickname").grid(row=1)
        self.entry_nickname = Entry(self, width=40)
        self.entry_nickname.grid(row=1, column=1, sticky=E+W, pady=(5,5))
        # email
        Label(self, text="Email").grid(row=2)
        self.entry_email = Entry(self, width=40)
        self.entry_email.grid(row=2, column=1, sticky=E+W, pady=(5,5))
        # login error display
        self.login_error = StringVar()
        Label(self, textvariable=self.login_error).grid(row=3,column=1,pady=(5,5))
        # connect
        self.login_button = Button(self, text="Login", command=self.login)
        self.login_button.grid(row=4, columnspan=3, pady=(5,5), padx=(5,5), sticky=N+S+E+W)

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
                    self.client.send_data(self.entry_name.get())
                    self.client.send_data(self.entry_nickname.get())
                    self.client.send_data(self.entry_email.get())

                    # receive user id
                    if self.client.receive_data():
                        # call main menu
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
        pass

    # method called when window is closed
    def window_closed(self):
        # close connection
        self.client.disconnect()

        # close window
        self.master.destroy()
        exit()