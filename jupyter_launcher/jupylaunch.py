import tkinter as tk
import configparser
from application import Application


import os

os.path.exists

CONSTS = {
    "JUPYLAUNCH_HOMEDIR" : ".jupylaunch",
    "SETTINGS_FILE" : "SETTINGS.conf",
    "SETTINGS_FILENAME_KEY" : "directories_filename"
}


def configure():
    homedir = os.path.expanduser("~")

    SETTINGS_FILE = CONSTS["SETTINGS_FILE"]
    SETTINGS_FILENAME_KEY = CONSTS["SETTINGS_FILENAME_KEY"]
    JUPYLAUNCH_HOMEDIR = CONSTS["JUPYLAUNCH_HOMEDIR"]




    config = configparser.ConfigParser()
    config.read(SETTINGS_FILE)

    if not "DEFAULT" in config:
        raise Exception("[DEFAULT] section not in {} file".format(SETTINGS_FILE))
    
    default_config = config["DEFAULT"]

    if not SETTINGS_FILENAME_KEY in default_config:
        raise Exception("directories_filename entry not in {} [DEFAULT] section".format(SETTINGS_FILE))


    directories_filename = default_config["directories_filename"].strip("\"")

    if not os.path.exists("{}/{}/".format(homedir, JUPYLAUNCH_HOMEDIR)):
        os.mkdir("{}/{}/".format(homedir, JUPYLAUNCH_HOMEDIR))

    if not os.path.exists("{}/{}/{}".format(homedir, JUPYLAUNCH_HOMEDIR, directories_filename)):
        filename = "{}/{}/{}".format(homedir, JUPYLAUNCH_HOMEDIR, directories_filename)
        
        try:
            f = open(filename, "w")
            f.close()
        except:
            print("Could not create file {}".format(filename))

    
    return config







if __name__ == "__main__":

    config = configure()

    root = tk.Tk()
    root.title("Jupyter Notebook Launcher")
    root.minsize(400, 300)

    app = Application(master=root, config=config, consts=CONSTS)
    app.mainloop()