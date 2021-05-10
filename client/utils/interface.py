from tkinter import *
from tkinter import ttk
import logging
import re
import json
import pickle
import pandas as pd
import io
from PIL import Image, ImageTk
from .client import Client

functions = [{"function": "confirmed", "name": "Confirmed objects", "description": "Get confirmed kepler objects", "parameters": False},
             {"function": "kepler_name", "name": "Search kepler names", "description": "Get kepler object by searching its name", "parameters": True},
             {"function": "koi_score", "name": "Kepler  certainty", "description": "Search based on certainty that koi object is a kepler object", "parameters": True},
             {"function": "countplot", "name": "Countplot disposition", "description": "Returns a countplot that shows how many koi objects where classified as kepler objects", "parameters": False},
             {"function": "scatterplot", "name": "Analyze correlation", "description": "Select two columns to see if they are correlated", "parameters": True}]

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
        self.entry_name = Entry(self, width=30)
        self.entry_name.grid(row=0, column=1, sticky=E+W, pady=(10,5),padx=(0,5))
        self.entries.append(self.entry_name)
        # nickname
        label = Label(self, text="Username")
        label.grid(row=1,padx=5,pady=5,sticky=W)
        self.labels.append(label)
        self.entry_uname = Entry(self, width=30)
        self.entry_uname.grid(row=1, column=1, sticky=E+W, pady=(5,5),padx=(0,5))
        self.entries.append(self.entry_uname)
        # email
        label = Label(self, text="Email")
        label.grid(row=2,padx=5,pady=5,sticky=W)
        self.labels.append(label)
        self.entry_email = Entry(self, width=30)
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
        if self.entry_name.get() and self.entry_uname.get() and self.entry_email.get():
            if not re.findall('[^a-zA-ZÀ-ÖØ-öø-ÿ\d\s:-]+', self.entry_name.get()):
                if not re.findall('[^a-zA-ZÀ-ÖØ-öø-ÿ\d\s:-]+', self.entry_uname.get()):
                    if re.match('([A-Za-z0-9.!#$%&*+\-/=?^_`{|}~]+@[A-Za-z0-9\-\.]+)', self.entry_email.get()):
                        logging.info("Login values valid")

                        # create socket and connect
                        self.client.connect()

                        # send user login data
                        data = f"login?fullname={self.entry_name.get()}&uname={self.entry_uname.get()}&email={self.entry_email.get()}"
                        self.client.send_data(data)

                        # receive user id
                        self.client.session_id = self.client.receive_data()
                    
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
        self.tabs = []
        tab_controller = ttk.Notebook(self.master)

        # create generals for each function
        for i in range(0, len(functions)):
            # create tab
            tab = ttk.Frame(tab_controller)
            self.tabs.append(tab)
            tab_controller.add(tab, text=functions[i]["name"])

            # button to send server request
            ttk.Label(tab, text=functions[i]["description"]).grid(column=0,row=0,padx=5,pady=5,sticky=W)
            sep = ttk.Separator(tab,orient='horizontal')
            sep.grid(column=0,columnspan=4,row=1,sticky=W+E)
            ttk.Button(tab, text="Send request", command=lambda i=i, tab=tab: self.append_main_menu(functions[i], tab)).grid(column=3,row=2,padx=10,pady=5,sticky=E)

        # specifics for get_kepler_name
        Label(self.tabs[1], text="Name to search").grid(column=0,row=2,padx=5,pady=5,sticky=W)
        self.search_name_entry = Entry(self.tabs[1], width=25)
        self.search_name_entry.grid(column=1,row=2,pady=5)

        # specifics for get_koi_score
        Label(self.tabs[2], text="Score").grid(column=0,row=2,padx=5,pady=5,sticky=W)
        self.search_score_entry = Entry(self.tabs[2], width=25)
        self.search_score_entry.grid(column=1,row=2,pady=5)
        choices = ('select search type', 'less then', 'less then or equal to', 'equal', 'greater then or equal to', 'greater then')             
        self.search_score_cbo = ttk.Combobox(self.tabs[2], state="readonly", width=25)        
        self.search_score_cbo['values'] = choices        
        self.search_score_cbo.current(0)
        self.search_score_cbo.grid(row=2, column=2, sticky=E+W)

        # specifics for scatterplot
        Label(self.tabs[4], text="Select columns").grid(column=0,row=2,padx=5,pady=5,sticky=W)
        # get column names
        self.client.send_data('column_names?')
        respose = self.client.receive_data()
        choices = []
        for choice in respose[1:-1].split(','):
            choices.append(choice.strip()[1:-1])

        self.scatterplot_x = ttk.Combobox(self.tabs[4], state="readonly", width=25)
        self.scatterplot_x['values'] = tuple(choices)
        self.scatterplot_x.grid(row=2, column=1, sticky=E+W)
        self.scatterplot_y = ttk.Combobox(self.tabs[4], state="readonly", width=25)
        self.scatterplot_y['values'] = tuple(choices)
        self.scatterplot_y.grid(row=2, column=2, sticky=E+W)

        # visualise tabs
        tab_controller.pack(expand=1, fill="both")

    # function request
    def function_request(self, function, parameters=None):
        # send data
        command = f"{function}?"
        if parameters:
            if function == "kepler_name":
                command += f"name={self.search_name_entry.get()}"
            elif function == "koi_score":
                search_dict = {'select search type': "lt", 'less then': "lt", 'less then or equal to': "le", 'equal':"eq", 'greater then or equal to': "ge", 'greater then':"gt"}
                command += f"score={self.search_score_entry.get()}&operand={search_dict[self.search_score_cbo.get()]}"
            elif function == 'scatterplot':
                command += f"x={self.scatterplot_x.get()}&y={self.scatterplot_y.get()}"


        self.client.send_data(command)

        # receive data and process
        if function == "confirmed" or function == "kepler_name" or function == "koi_score":
            result = pickle.loads(eval(self.client.receive_data()))
        else:
            result = b''.join(eval(self.client.receive_data()))
            result = Image.open(io.BytesIO(result))
        return result

    # add data to window
    def append_main_menu(self, function, tab):
        self.data = self.function_request(function['function'], function['parameters'])

        if function['function'] == "confirmed" or function['function'] == "kepler_name" or function['function'] == "koi_score":
            # add listbox + scrollbar
            self.scrollbar = Scrollbar(tab, orient=VERTICAL)
            self.datalst = Listbox(tab, yscrollcommand=self.scrollbar.set)
            self.scrollbar.config(command=self.datalst.yview)
            # positioning
            self.datalst.grid(column=0,row=3,rowspan=3,padx=5,pady=5,sticky=N+W+S)
            self.scrollbar.grid(column=0,row=3,rowspan=3,sticky=N+S+E)
            # add data to listbox + add functionality
            for item in range(0,len(self.data["kepler_name"])-1):
                self.datalst.insert(END, self.data.iloc[item]["kepler_name"]) if not isinstance(self.data.iloc[item]["kepler_name"],float) else self.datalst.insert(END, self.data.iloc[item]["kepoi_name"])
            self.datalst.bind('<<ListboxSelect>>', self.onselect_datalst)

            # placeholders for selected data
            self.selected = StringVar()

            Label(tab, text="Selected:").grid(column=1,row=3,padx=5,sticky=W)
            Label(tab, textvariable=self.selected).grid(column=2,row=3,sticky=W)

            if function['function'] == 'koi_score':
                self.koi_score = StringVar()
                Label(tab, text="Koi score:").grid(column=1,row=4,padx=5,sticky=W)
                Label(tab, textvariable=self.koi_score).grid(column=2,row=4,sticky=W)
                self.koi_disposition = StringVar()
                Label(tab, text="Koi disposition:").grid(column=1,row=5,padx=5,sticky=W)
                Label(tab, textvariable=self.koi_disposition).grid(column=2,row=5,sticky=W)
            else:
                # star size
                self.star_size = StringVar()
                Label(tab, text="Star size:").grid(column=1,row=4,padx=5,sticky=W)
                Label(tab, textvariable=self.star_size).grid(column=2,row=4,sticky=W)
                # temperature
                self.temperature = StringVar()
                Label(tab, text="Temperature:").grid(column=1,row=5,padx=5,sticky=W)
                Label(tab, textvariable=self.temperature).grid(column=2,row=5,sticky=W)
                # # distance
                # self.koi_score = StringVar()
                # Label(tab, text="Koi score:").grid(column=1,row=4,padx=5,sticky=W)
                # Label(tab, textvariable=self.koi_score).grid(column=2,row=4,sticky=W)
                # # other
                # self.koi_score = StringVar()
                # Label(tab, text="Koi score:").grid(column=1,row=4,padx=5,sticky=W)
                # Label(tab, textvariable=self.koi_score).grid(column=2,row=4,sticky=W)

        elif function['function'] == 'countplot' or function['function'] == 'scatterplot':
            self.img_placholder = Label(tab)
            self.img_placholder.grid(column=0,row=3,padx=5,pady=5,sticky=N+W+S+E)

            self.img = ImageTk.PhotoImage(self.data)
            self.img_placholder['image'] = self.img

    def onselect_datalst(self, event):
        index = int(self.datalst.curselection()[0])
        value = self.datalst.get(index)
        logging.debug('You selected item %d: "%s"' % (index, value))
        self.selected.set(value)

        if self.koi_score:
            if "Kepler" in value:
                self.koi_score.set(self.data.loc[self.data['kepler_name'] == value, 'koi_score'].iloc[0])
                self.koi_disposition.set(self.data.loc[self.data['kepler_name'] == value, 'koi_disposition'].iloc[0])
            else:
                self.koi_score.set(self.data.loc[self.data['kepoi_name'] == value, 'koi_score'].iloc[0])
                self.koi_disposition.set(self.data.loc[self.data['kepoi_name'] == value, 'koi_disposition'].iloc[0])
        else:
            self.temperature.set(self.data.loc[self.data['kepler_name'] == value, 'koi_teq'].iloc[0])
            self.star_size.set(self.data.loc[self.data['kepler_name'] == value, 'koi_srad'].iloc[0])

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