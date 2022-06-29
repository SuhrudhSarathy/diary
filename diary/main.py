from create_files import *
from init import *
from list_functions import *
from print_color import *

import os
import argparse

"""Goal of the file:
1. Should be able to initialise a diary in any folder
"""

help_str = "Main command to run. Available commands are init, new, list, update"

parser = argparse.ArgumentParser(prog="diary", description="Log your daily tasks in Markdown format", add_help=True)

parser.add_argument("command", help=help_str, default="none", nargs="?")


# Optional Arguments
parser.add_argument("-e", "--explain", help="Ask for help on any command")
parser.add_argument("-y", "--year", help="Specify the year", type=int)
parser.add_argument("-m", "--month", help="Specify the month")
parser.add_argument("-t", "--tag", help="Specify the tag for search")

args = parser.parse_args()
if args.command == "init":
    initialise_diary()

elif args.command == "new":
    # Handle the month and year using positional arguments
    month = args.month
    year = args.year

    create_files(year, month)

elif args.command == "list":
    tag = args.tag

    get_list_tag(tag)
    
elif args.command == "update":
    update()

# Explain
if args.explain== "init":
    parser.print_help()
    prGreen("Explanation:\n\tThe `init` command initialises the diary.")
elif args.explain == "new":
    parser.print_help()
    prGreen("Explanation:\n\tThe `new` command creates new diary entries.")
elif args.explain == "update":
    parser.print_help()
    prGreen("Explanation:\n\tThe `update` command updates the record for all files and tags.")