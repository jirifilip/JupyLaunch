import tkinter as tk
from tkinter.filedialog import askdirectory

import sys
import os

from multiprocessing import Process
import subprocess
import shlex

from directory_popup import DirectoryPopup



WINDOW_SIZE = 500, 500
STRETCH = tk.W + tk.E + tk.N + tk.S

class NotADirectoryException(Exception):
    pass

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.configure_startup()
        self.pack()

        self.create_widgets()



    def configure_startup(self):
        self.load_directories()


    def load_directories(self):
        self.filename = "directories.txt"

        self.directories = []

        try:
            with open(self.filename) as f:
                lines = f.read().splitlines()

                for line in lines:
                    if not os.path.isdir(line):
                        raise NotADirectoryException
                    
                    self.directories.append(line)

                
                



        except NotADirectoryException as e:
            print("Not a directory")
        except Exception as e:
            print(e)


    def create_widgets(self):

        self.launch_button = tk.Button(self)
        self.launch_button["text"] = "Launch"
        self.launch_button["command"] = self.launch_jupyter


        self.add_button = tk.Button(self)
        self.add_button["text"] = "Add directory"
        self.add_button["command"] = self.directory_add_clicked
        

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        
        
        self.create_directories_buttons()


        self.dir_listbox.grid(row=0, column=0, columnspan=2, sticky=STRETCH)
        self.add_button.grid(row=1, columnspan=2, sticky=STRETCH)
        self.launch_button.grid(row=2, column=0, sticky=STRETCH)
        self.quit.grid(row=2, column=1, sticky=STRETCH)
        

    def create_directories_buttons(self):
        self.dir_listbox = tk.Listbox(self)

        for directory in self.directories:
            self.dir_listbox.insert(tk.END, directory)


        self.dir_listbox.pack()
        

    def directory_add_clicked(self):
        #dirname = self.directory_popup()
        dirname = askdirectory(title="Choose a directory")

        if os.path.isdir(dirname):
            self.dir_listbox.insert(tk.END, dirname)

            with open(self.filename, "a") as f:
                f.write("\n{}".format(dirname))

    def directory_popup(self):
        param = { "dir" : None }

        self.add_window = DirectoryPopup(self.master, param, "dir")

        self.master.wait_window(self.add_window)

        print(param["dir"])

        return param["dir"]




    def launch_jupyter(self):
        current_selection = self.dir_listbox.curselection()

        idx = current_selection[0]

        launch_dir = self.directories[idx]

        def jupyter_process():
            command = "jupyter notebook --notebook-dir={}".format(launch_dir)

            subprocess.Popen(shlex.split(command))

        
        jupyter_process()
        








root = tk.Tk()
app = Application(master=root)
app.mainloop()