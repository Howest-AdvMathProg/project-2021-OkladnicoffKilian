from tkinter import *
import logging
import threading
import re
from os import path

class Interface(Frame):
    def __init__(self, command_class, master=None):
        # set variables
        Frame.__init__(self, master)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.window_closed)
        self.command_class = command_class
        self.selected = None

        self.pack(fill=BOTH, expand=1)

        # call content creator
        self.content()
        self.update()

    def update(self):
        self.clientlst.delete(0, 'end')
        [self.clientlst.insert('end', i) for i in [k for k in self.command_class.logged_in]]
        
        self.master.after(1000, self.update)

    def send_message(self, guid, msg):
        if guid in self.command_class.logged_in.keys():
            self.command_class.logged_in[guid]['socket'].send(msg)

    def filter_logs(self, guid):
        user = self.command_class.logged_in[guid]["username"]
        fp = path.join(path.dirname(__file__), "../logs/Commands.log")
        if path.exists(fp):
            entries = []
            with open(fp, 'r') as fo:
                [entries.append(line) for line in fo if re.match(f"\[.*\] {guid}\({user}\)", line)]
                fo.close()
            return entries

    def start_messaging(self):
        if not self.selected:
            print("no client selected")
            return
        print("started message")

    def view_user_logs(self):
        if not self.selected:
            print("no client selected")
            return
        data = self.filter_logs(self.selected)

    def content(self):
        self.master.title("Server")

        # client select
        Label(self, text="Connected clients").grid(column=0,row=0,padx=15,pady=10)
        # list of connected clients
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.clientlst = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.clientlst.yview)
        
        self.clientlst.grid(column=0,row=1,rowspan=10,pady=(0,10), sticky=N+S+E+W)
        self.scrollbar.grid(column=0,row=1,rowspan=10, sticky=N+S+E)
        # fill listbox with connected clients
        self.clientlst.bind('<<ListboxSelect>>', self.on_client_select)


        # info selected client
        Label(self, text="Selected client").grid(column=1,row=0,padx=15,pady=10)
        Label(self, text="Session id:").grid(column=1,row=1,padx=15,pady=(0,10))
        Label(self, text="Full name:").grid(column=1,row=2,padx=15,pady=(0,10))
        Label(self, text="Nickname:").grid(column=1,row=3,padx=15,pady=(0,10))
        Label(self, text="Email:").grid(column=1,row=4,padx=15,pady=(0,10))
        # selected variables and labels
        self.client_session_id = StringVar()
        self.client_fullname = StringVar()
        self.client_username = StringVar()
        self.client_email = StringVar()
        self.lbl_client_session_id = Label(self, textvariable=self.client_session_id).grid(column=2,row=1,padx=15,pady=(0,10))
        self.lbl_client_fullname = Label(self, textvariable=self.client_fullname).grid(column=2,row=2,padx=15,pady=(0,10))
        self.lbl_client_username = Label(self, textvariable=self.client_username).grid(column=2,row=3,padx=15,pady=(0,10))
        self.lbl_client_email = Label(self, textvariable=self.client_email).grid(column=2,row=4,padx=15,pady=(0,10))


        # connect to client button
        Button(self, text="Message client").grid(column=1,columnspan=2,row=5)

        # grid configuration
        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self, 3, weight=1)

    # gets called when a item in clientlst is selected
    def on_client_select(self, event):
        if len(self.clientlst.curselection()) > 0:
            self.selected = self.clientlst.get(self.clientlst.curselection()[0])
            user = self.command_class.logged_in[self.selected]
            self.client_session_id.set(self.selected)
            self.client_username.set(user['username'])
            self.client_fullname.set(user['fullname'])
            self.client_email.set(user['email'])
            

    def window_closed(self):
        exit()