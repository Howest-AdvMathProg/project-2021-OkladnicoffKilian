import tkinter

class Interface(tkinter.Frame):
    def __init__(self, master):
        super().__init__(master=master)

if __name__ == "__main__":
    root = tkinter.Tk()
    
    i = Interface(root)
    i.mainloop()