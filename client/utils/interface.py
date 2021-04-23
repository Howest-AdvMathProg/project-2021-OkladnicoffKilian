from tkinter import *
import logging
import socket
import re

class Interface(Frame):
    def __init__(self, master=None):
        # set variables
        Frame.__init__(self, master)
        self.master = master

        # root = Tk()
        # root.mainloop()

        self.master.protocol("WM_DELETE_WINDOW", self.window_closed)

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
        # connect
        self.login_button = Button(self, text="Login", command=self.login)
        self.login_button.grid(row=3, columnspan=2, pady=(5,5), padx=(5,5), sticky=N+S+E+W)

        # grid config
        Grid.rowconfigure(self, 4, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

    def login(self):
        # validate inputs
        if self.entry_name.get():
            if self.entry_nickname.get():
                if re.match('([A-Za-z0-9.!#$%&*+\-/=?^_`{|}~]+@[A-Za-z0-9\-\.]+)', self.entry_email.get()):
                    logging.info("Login values valid")
                    # create connection

                    # send user login data

                    # receive user id

                    # call main menu
                else:
                    logging.error("Invalid email")
            else:
                logging.error("Invalid nickname: nickname cannot be empty")
        else:
            logging.error("Invalid name: full name cannot be empty")

    # method called when window is closed
    def window_closed(self):
        # close connection
        # self.socket_to_server.close()
        logging.info("Connection closed with server")

        # close window
        self.master.destroy()
        exit()