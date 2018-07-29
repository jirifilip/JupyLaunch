import tkinter as tk

class DirectoryPopup(tk.Frame):

    def __init__(self, master, param_dict, key):
        super().__init__(master)
        self.top = tk.Toplevel(master)

        self.param_dict = param_dict
        self.key = key

        self.label = tk.Label(self.top, text="Enter a directory name.")
        self.label.pack()
        
        self.entry = tk.Entry(self.top)
        self.entry.pack()
        
        self.button = tk.Button(self.top, text='Add directory', command=self.cleanup)
        self.button.pack()
    
    def cleanup(self):
        self.value = self.entry.get()
        self.param_dict[self.key] = self.value

        self.top.destroy()
        self.destroy()