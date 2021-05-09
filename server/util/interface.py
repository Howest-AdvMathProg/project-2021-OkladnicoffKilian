from tkinter import *
import logging

class Interface(Frame):
    def __init__(self, master=None):
        # set variables
        Frame.__init__(self, master)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.window_closed)

        self.pack(fill=BOTH, expand=1)

        # call content creator
        self.content()

    def content(self):
        self.master.title("Server")

        # client select
        Label(self, text="Connected clients").grid(column=0,row=0,padx=15,pady=10)
        # list of connected clients
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.clientlst = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.clientlst.yview)
        
        self.clientlst.grid(column=0,row=1,rowspan=4,pady=(0,10), sticky=N+S+E+W)
        self.scrollbar.grid(column=0,row=1,rowspan=4, sticky=N+S+E)
        # fill listbox with connected clients
        # self.clientlst.bind('<<ListboxSelect>>', self.on_client_select)


        # info selected client
        Label(self, text="Selected client").grid(column=1,row=0,padx=15,pady=10)
        Label(self, text="Full name:").grid(column=1,row=1,padx=15,pady=(0,10))
        Label(self, text="Nickname:").grid(column=1,row=2,padx=15,pady=(0,10))
        Label(self, text="Email:").grid(column=1,row=3,padx=15,pady=(0,10))
        # selected variables and labels
        self.client_fullname = StringVar()
        self.client_username = StringVar()
        self.client_email = StringVar()
        self.lbl_client_fullname = Label(self, textvariable=self.client_fullname).grid(column=2,row=1,padx=15,pady=(0,10))
        self.lbl_client_username = Label(self, textvariable=self.client_username).grid(column=2,row=2,padx=15,pady=(0,10))
        self.lbl_client_email = Label(self, textvariable=self.client_email).grid(column=2,row=3,padx=15,pady=(0,10))


        # connect to client button
        Button(self, text="Message client").grid(column=1,columnspan=2,row=4)

        # grid configuration
        Grid.rowconfigure(self, 5, weight=1)
        Grid.columnconfigure(self, 3, weight=1)

    # gets called when a item in clientlst is selected
    def on_client_select(self, event):
        index = int(self.clientlst.curselection()[0])
        value = self.clientlst.get(index)
        logging.debug(f"Selected client {index}: {value}")

    def window_closed(self):
        exit()