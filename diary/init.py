"""This file will be called when the `diary init` command will be called
On initialisation:
    1. create a .diary folder
"""
import os
import datetime

def initialise_diary() :
    pwd = os.getcwd()

    try:
        os.mkdir(os.path.join(pwd, ".diary"))
        with open(os.path.join(pwd, ".diary/date.txt"), "w") as file:
            file.write(str(datetime.date.today()))
    except FileExistsError:
        with open(os.path.join(pwd, ".diary/date.txt"), "r") as file:
            data = file.readlines()
        date = data[0]
        print(f"Diary already exists. Diary was created on {date}")
    except FileNotFoundError:
        raise Exception("Folder not found. Something is wrong. This shouldn't happen")

if __name__ == "__main__":
    initialise_diary()