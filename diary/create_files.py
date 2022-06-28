"""File that contains functions to generate files, folders etc"""
import os
import datetime
import calendar

months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
        }

days = ["Mon", "Tue", "Wed", "Thurs", "Fri", "Sat", "Sun"]

material = """---
date: DATE
day: DAY
tag:
description:
---

# DATE
## ToDo
- [ ] Task 1
- [ ] Task 2

"""

def generate_text(date: str, day: int)->str:
    string = material.replace("DATE", date)
    string = string.replace("DAY", str(days[day]))

    return string


def create_week_folders(folder_path, n):
    """Function to create week folder in a give path
    Args:
        folder_path: path to folder
        n: number of weeks
    """
    for i in range(n):
        try:
            os.mkdir(os.path.join(folder_path, f"Week {i+1}"))
        except FileExistsError:
            # The folder already exist, ignore
            pass
        except FileNotFoundError:
            # Cannot create folder here
            raise Exception("Cannot create folder here. Check path once")


def create_files(year, month, **kwargs):
    """Creates the required files for the given (year, month).
    The format of the folder is as follows:
    month/
        week1/
            dd-mm-yy.md
            dd-mm-yy.md
            ...
        week2/
            dd-mm-yy.md
            dd-mm-yy.md
            ...
    Args:
        year: int
        month: str
    kwargs:
        include_weekends: bool = False, default
    """
    if len(month) > 3:
        month = month[:3].title()
    try:
        include_weekends = kwargs['include_weekends']
    except KeyError:
        include_weekends = False

    # Check if the pwd contains a .diary folder
    folders_in_path = os.listdir()
    if ".diary" in folders_in_path:
        # Create the main Month folder
        month_path = os.path.join(os.getcwd(), month) 
        # Exception handling
        try:
            os.mkdir(month_path)
            with open(os.path.join(os.getcwd(), ".diary/months.txt"), "a+") as file:
                file.write(str(month_path) + "\n")

        except FileExistsError:
            # The folder already exist, ignore
            pass
        except FileNotFoundError:
            # Cannot create folder here
            raise Exception("Cannot create folder here. Check path once")

        month_cal = calendar.monthcalendar(year, months[month])

        # make the week folders
        create_week_folders(month_path, len(month_cal))

        # get the week folders
        week_folders = sorted(os.listdir(month_path))

        for w, week in enumerate(month_cal):
            for i, date in enumerate(week):
                if not include_weekends:
                    if date != 0 and (i != 5 and i != 6):
                        # this is to handle empty dates in the week
                        date = f"{date}-{months[month]}-{year}"
                        file_str = generate_text(date, i)
                        file_path = os.path.join(month_path, week_folders[w], date+".md")
                        if f"{date}.md" in os.listdir(os.path.join(month_path, week_folders[w])):
                            raise Exception("File already exists. Continuing will cause rewriting every file. To rewrite everything use `diary clean` in the directory")
                        with open(file_path, "w") as file:
                            file.write(file_str)
                else:
                    if date != 0:
                        date = f"{date}-{months[month]}-{year}"
                        file_str = generate_text(date, i)
                        file_path = os.path.join(month_path, week_folders[w], date+".md")
                        if f"{date}.md" in os.listdir(os.path.join(month_path, week_folders[w])):
                            raise Exception("File already exists. Continuing will cause rewriting every file. To rewrite everything use `diary clean` in the directory")
                        with open(file_path, "w") as file:
                            file.write(file_str)
    else:
        raise Exception(".diary folder not found. Did you initialise the diary?")

if __name__ == "__main__":
    create_files(2022, "June")