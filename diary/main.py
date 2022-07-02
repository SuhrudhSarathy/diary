from functions import *

import os
import argparse

"""Goal of the file:
1. Should be able to initialise a diary in any folder
"""

help_str = "Main command to run. Available commands are init, new, list, update"

parser = argparse.ArgumentParser(prog="diary", description="Log your daily tasks in Markdown format", add_help=True)

parser.add_argument("command", help=help_str, default="none", nargs="?")
parser.add_argument("option", help="Supporting option to a command", default="none", nargs="?")


# Optional Arguments
parser.add_argument("-e", "--explain", help="Ask for help on any command. Eg `diary -e new`")
parser.add_argument("-y", "--year", help="Specify the year", type=int)
parser.add_argument("-m", "--month", help="Specify the month")
parser.add_argument("-f", "--file", help="Insert the file location")

args = parser.parse_args()
if args.command == "init":
    initialise_diary()

elif args.command == "new":
    # Handle the month and year using positional arguments
    month = args.month
    year = args.year
    file_location = args.file

    create_files(year, month, file_location)

elif args.command == "list":
    tag = args.option

    get_list_tag(tag)
    
elif args.command == "update":
    update()

else:
    parser.print_help()

# For explain
# Explain
if args.explain== "init":
    parser.print_help()
    prGreen("Explanation:\n\tThe `init` command initialises the diary.")
elif args.explain == "new":
    parser.print_help()
    prGreen("Explanation:\n\tThe `new` command creates new diary entries.\n Example:")
    prCyan("\tdiary new -m Jul -y 2022")
    prCyan("\tdiary new -m Jan -y 2021 -f experiment.md")

elif args.explain == "list":
    parser.print_help()
    prGreen("Explanation:\n\tThe `list` command lists the entries with a give tag.\n Example:")
    prCyan("\tdiary list ml")
    prCyan("\tdiary list robotics")

elif args.explain == "update":
    parser.print_help()
    prGreen("Explanation:\n\tThe `update` command updates the record for all files and tags.")