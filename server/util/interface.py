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
        
        self.reqlst.delete(0, 'end')
        [self.reqlst.insert('end', f"{k} | {v} times called") for k,v in sorted(self.command_class.get_endpoint_counts().items(), key=lambda x: x[1], reverse=True)]
        
        try:
            self.userloglst.delete(0, 'end')
            [self.userloglst.insert('end', i) for i in self.filter_logs(self.selected)]
        except:
            pass

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
        self.send_message(self.selected, "test")

    def content(self):
        self.master.title("Server")

        # client select
        Label(self, text="Connected clients").grid(column=0,row=0,padx=5,pady=10,sticky=W)
        # list of connected clients
        self.client_scrollbar = Scrollbar(self, orient=VERTICAL)
        self.clientlst = Listbox(self, yscrollcommand=self.client_scrollbar.set,width=30)
        self.client_scrollbar.config(command=self.clientlst.yview)
        
        self.clientlst.grid(column=0,row=1,rowspan=5,pady=(0,10), sticky=N+S+W)
        self.client_scrollbar.grid(column=0,row=1,rowspan=5, sticky=N+S+E)
        # fill listbox with connected clients
        self.clientlst.bind('<<ListboxSelect>>', self.on_client_select)

        # function usage
        Label(self, text="Request counters").grid(column=0,row=6,padx=5,pady=5,sticky=W)
        self.counter_scrollbar = Scrollbar(self, orient=VERTICAL)
        self.reqlst = Listbox(self, yscrollcommand=self.counter_scrollbar.set,width=30)
        self.counter_scrollbar.config(command=self.reqlst.yview)

        self.reqlst.grid(column=0,row=7,rowspan=2,pady=(0,10), sticky=N+S+W)
        self.counter_scrollbar.grid(column=0,row=7,rowspan=2, sticky=N+S+E)
        # fill listbox with request stuff
        
        # info selected client
        Label(self, text="Selected client").grid(column=1,row=0,padx=15,pady=10,sticky=W)
        Label(self, text="Session id:").grid(column=1,row=1,padx=15,pady=(0,5),sticky=W)
        Label(self, text="Full name:").grid(column=1,row=2,padx=15,pady=(0,5),sticky=W)
        Label(self, text="Nickname:").grid(column=1,row=3,padx=15,pady=(0,5),sticky=W)
        Label(self, text="Email:").grid(column=1,row=4,padx=15,pady=(0,5),sticky=W)
        # selected variables and labels
        self.client_session_id = StringVar()
        self.client_fullname = StringVar()
        self.client_username = StringVar()
        self.client_email = StringVar()
        self.lbl_client_session_id = Label(self, textvariable=self.client_session_id,width=30).grid(column=2,row=1,padx=15,pady=(0,10),sticky=W)
        self.lbl_client_fullname = Label(self, textvariable=self.client_fullname).grid(column=2,row=2,padx=15,pady=(0,10),sticky=W)
        self.lbl_client_username = Label(self, textvariable=self.client_username).grid(column=2,row=3,padx=15,pady=(0,10),sticky=W)
        self.lbl_client_email = Label(self, textvariable=self.client_email).grid(column=2,row=4,padx=15,pady=(0,10),sticky=W)


        # connect to client button
        Button(self, text="Message client", command=self.start_messaging).grid(column=1,row=5)
        Button(self, text="Show logged commands", command=self.show_userlogs).grid(column=2,row=5,sticky=W)

        # grid configuration
        Grid.rowconfigure(self, 10, weight=1)
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
            
    def show_userlogs(self):
        # user logs
        Label(self, text="User logs").grid(column=1,row=6,padx=5,pady=5,sticky=W)
        self.userlog_scrollbar = Scrollbar(self, orient=VERTICAL)
        self.userloglst = Listbox(self, yscrollcommand=self.userlog_scrollbar.set,width=100)
        self.userlog_scrollbar.config(command=self.userloglst.yview)

        self.userloglst.grid(column=1,columnspan=2,row=7,rowspan=2,padx=(5,20),pady=(0,10), sticky=N+S+W)
        self.userlog_scrollbar.grid(column=1,columnspan=2,row=7,rowspan=2,pady=(0,5), sticky=N+S+E)

    def window_closed(self):
        exit()