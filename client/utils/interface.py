from tkinter import *
from tkinter import ttk
import logging
import re
import json
from .client import Client

functions = ["Seach kepler name", "scatterplot", "false positives vs true positives", "random kepler object"]

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
        label.grid(row=0,padx=5,pady=5,sticky=W)
        self.labels.append(label)
        self.entry_name = Entry(self, width=40)
        self.entry_name.grid(row=0, column=1, sticky=E+W, pady=(10,5),padx=(0,5))
        self.entries.append(self.entry_name)
        # nickname
        label = Label(self, text="Nickname")
        label.grid(row=1,padx=5,pady=5,sticky=W)
        self.labels.append(label)
        self.entry_nickname = Entry(self, width=40)
        self.entry_nickname.grid(row=1, column=1, sticky=E+W, pady=(5,5),padx=(0,5))
        self.entries.append(self.entry_nickname)
        # email
        label = Label(self, text="Email")
        label.grid(row=2,padx=5,pady=5,sticky=W)
        self.labels.append(label)
        self.entry_email = Entry(self, width=40)
        self.entry_email.grid(row=2, column=1, sticky=E+W, pady=(5,5),padx=(0,5))
        self.entries.append(self.entry_email)
        # login error display
        self.login_error = StringVar()
        label = Label(self, textvariable=self.login_error)
        label.grid(row=3,column=0,columnspan=2)
        self.labels.append(label)
        # connect
        self.login_button = Button(self, text="Login", command=self.login)
        self.login_button.grid(row=4, columnspan=2, pady=(5,5), padx=(5,5), sticky=N+S+E+W)
        self.buttons.append(self.login_button)

        # grid config
        Grid.rowconfigure(self, 4, weight=1)
        Grid.columnconfigure(self, 2, weight=1)

    def login(self):
        # validate inputs
        # check if not empty
        if self.entry_name.get() and self.entry_nickname.get() and self.entry_email.get():
            print(re.findall('[^a-zA-ZÀ-ÖØ-öø-ÿ\d\s:-]+', self.entry_name.get()))
            if not re.findall('[^a-zA-ZÀ-ÖØ-öø-ÿ\d\s:-]+', self.entry_name.get()):
                if not re.findall('[^a-zA-ZÀ-ÖØ-öø-ÿ\d\s:-]+', self.entry_nickname.get()):
                    if re.match('([A-Za-z0-9.!#$%&*+\-/=?^_`{|}~]+@[A-Za-z0-9\-\.]+)', self.entry_email.get()):
                        logging.info("Login values valid")

                        # create socket and connect
                        self.client.connect()

                        # send user login data
                        data = f"login?fullname={self.entry_name.get()}&username={self.entry_nickname.get()}&email={self.entry_email.get()}"
                        self.client.send_data(data)

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
                    logging.error("Invalid nickname")
                    self.login_error.set("Invalid nickname")
            else:
                logging.error("Invalid name")
                self.login_error.set("Invalid full name")
        else:
            logging.error("All fields must be filled in")
            self.login_error.set("All fields must be filled in")

    # main menu
    def main_menu(self):
        Label(self, text="Connected to server").grid(row=0,column=0,padx=5)
        # logout button
        logout_button = Button(self, text="Logout", command=self.window_closed)
        logout_button.grid(row=0, column=3, pady=(5,5), padx=(5,5), sticky=N+S+E+W)

        # create parent for tabs
        tab_controller = ttk.Notebook(self.master)

        # create generals for each function
        for i in range(0, len(functions)-1):
            # create tab
            tab = ttk.Frame(tab_controller)
            tab_controller.add(tab, text=f"Tab {i}")

            # button to send server request
            ttk.Label(tab, text=f"Function {i}: {functions[i]}").grid(column=0,row=0,padx=5,pady=5,sticky=W)
            ttk.Button(tab, text="Command", command=lambda i=i: self.function_request(i)).grid(column=3,row=0,padx=10,pady=5)

        # visualise tabs
        tab_controller.pack(expand=1, fill="both")

    # function request
    def function_request(self, tab_number):
        logging.debug(f"Request came from tab {tab_number}")
        logging.debug(f"Function: {functions[tab_number]}")

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