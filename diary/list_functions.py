"""File contains functions that can be used to list down the files and their descriptions given arguments"""
from print_color import *
import os

def get_list_tag(tag):
    # Gets the list of all the entires with a particular tag
    tags = os.listdir(".diary/tags")
    tags = [t.replace(".txt", "") for t in tags]

    if tag not in tags:
        prRed("Did not find the listed tag", end="")
        prCyan(f"`tag`")
        prRed("Use the command ", end="")
        prCyan("`diary update` ", end="")
        prRed("to update the list")
    
    else:
        prRed(f"This is a list of all the entries with the tag", end="")
        prCyan(f"`tag`")
        tag_file = os.path.join(".diary/tags", tag + ".txt")

        with open(tag_file, "r") as file:
            lines = file.readlines()
        
        for line in lines:
            line = line.replace("\n", "")
            line = line.split("^&*")
            filename, tag, desc = line
            filename = filename.split("/")[-1].replace(".md", "")
            prCyan(filename, ": ")
            prGreen(tag, " ")
            prPurple(desc)

        print()
        prRed("Use the command ", end="")
        prCyan("`diary update` ", end="")
        prRed("to update the list")

if __name__ == "__main__":
    get_list_tag("env")