import tkinter as tk
from tkinter.filedialog import askdirectory

import sys
import os

from multiprocessing import Process
import subprocess
import shlex

STRETCH = tk.W + tk.E + tk.N + tk.S

class NotADirectoryException(Exception):
    pass

class Application(tk.Frame):
    def __init__(self, master=None, config=None, consts={}):
        super().__init__(master)

        self.config = config
        self.CONSTS = consts
        self.master = master
        self.configure_startup()
        self.pack()

        self.create_widgets()



    def configure_startup(self):
        self.load_directories()


    def load_directories(self):
        filename_key = self.CONSTS["SETTINGS_FILENAME_KEY"]

        self.filename = "{}/{}/{}".format(
            os.path.expanduser("~"),
            self.CONSTS["JUPYLAUNCH_HOMEDIR"],
            self.config["DEFAULT"][filename_key]
        )

        self.directories = []

        try:
            with open(self.filename) as f:
                lines = f.read().splitlines()

                for line in lines:
                    if not os.path.isdir(line):
                        raise NotADirectoryException
                    
                    self.directories.append(line)

                
                
        except NotADirectoryException as e:
            print("Problem parsing the directory file.")
            print(e)
        except Exception as e:
            print(e)


    def create_widgets(self):

        self.launch_button = tk.Button(self)
        self.launch_button["text"] = "Launch"
        self.launch_button["command"] = self.launch_jupyter

        
        self.add_button = tk.Button(self)
        self.add_button["text"] = "Add directory to list"
        self.add_button["command"] = self.directory_add_clicked

        self.remove_button = tk.Button(self)
        self.remove_button["text"] = "Remove directory from list"
        self.remove_button["command"] = self.directory_remove_clicked
        

        self.quit = tk.Button(self, text="Quit", command=self.master.destroy)
        
        
        self.create_directories_buttons()


        self.dir_listbox.grid(row=0, column=0, columnspan=2, sticky=STRETCH)
        self.add_button.grid(row=1, columnspan=2, sticky=STRETCH)
        self.remove_button.grid(row=2, columnspan=2, sticky=STRETCH)        
        self.launch_button.grid(row=3, column=0, sticky=STRETCH)
        self.quit.grid(row=3, column=1, sticky=STRETCH)
        

    def create_directories_buttons(self):
        self.dir_listbox = tk.Listbox(self)

        for directory in self.directories:
            self.dir_listbox.insert(tk.END, directory)


        self.dir_listbox.pack()
        

    def directory_add_clicked(self):
        dirname = askdirectory(title="Choose a directory", initialdir=os.path.expanduser("~"))

        if os.path.isdir(dirname):
            self.directories.append(dirname)
            self.dir_listbox.insert(tk.END, dirname)

            self.write_dirnames()


    def directory_remove_clicked(self):
        idx = self.dir_listbox.curselection()[0]
        
        self.dir_listbox.delete(idx)
        del self.directories[idx]
        

        self.write_dirnames()



    def write_dirnames(self):
        new_file_text = "\n".join(self.directories)

        with open(self.filename, "w") as f:
            f.write(new_file_text)
        



    def launch_jupyter(self):
        current_selection = self.dir_listbox.curselection()

        idx = current_selection[0]

        launch_dir = self.directories[idx]

        def jupyter_process():
            command = "jupyter notebook --notebook-dir={}".format(launch_dir)

            subprocess.Popen(shlex.split(command))

        
        jupyter_process()