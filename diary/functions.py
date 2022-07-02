import os
import datetime
import calendar

from print_color import *

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

def initialise_diary() :
    pwd = os.getcwd()

    try:
        os.mkdir(os.path.join(pwd, ".diary"))
        os.mkdir(os.path.join(pwd, ".diary", "tags"))
        with open(os.path.join(pwd, ".diary/date.txt"), "w") as file:
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            file.write(dt_string+"\n")
            prCyan(f"Diary Initialised on {dt_string}")
    except FileExistsError:
        with open(os.path.join(pwd, ".diary/date.txt"), "r") as file:
            data = file.readlines()
        date = data[0]
        date = date.replace("\n", "")
        prRed(f"Diary already exists. Diary was created on {date}")
    except FileNotFoundError:
        raise Exception("Folder not found. Something is wrong. This shouldn't happen")

def update():
    """Used to update .diary folder to contain the updated list of tags etc
    The .diary/tags contains files that has a list of files that store location of the files

    Process:
        1. Search through the diary into all files and gets the tag and description and stores it in a file
        2. Write the last updated date in the .diary/date.txt file
    """

    # Write the last updated date into the date file
    with open(".diary/date.txt", "r") as file:
        lines = file.readlines()

    with open(".diary/date.txt", "w") as file:
        try:
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            lines[1] = dt_string
        except IndexError:
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            lines.append(dt_string)
        finally:
            file.writelines(lines)

    months_in_diary = os.listdir()

    tag_dict = {}

    # Get the files in the tag folder
    tag_files = os.listdir(".diary/tags")
    if (len(tag_files)) == 0:
        prGreen("No tag files detected. Creating files after update")
    
    else:
        for f in tag_files:
            tag = f.replace(".txt", "")
            tag_dict[tag] = []

    for month in months_in_diary:
        if month in months.keys():
            month_path = os.path.join(os.getcwd(), month)

            # get the weeks in the months
            weeks = sorted(os.listdir(month_path))

            for week in weeks:
                week_path = os.path.join(month_path, week)
                
                days = os.listdir(week_path)

                for day in days:
                    day_path = os.path.join(week_path, day)

                    # Open the file using day_path
                    with open(day_path, "r") as file:
                        lines = file.readlines()
                        # There is an assumption that the 4th line is tag and the 5th is description
                        # This is hard coded for now. Don't change the metadata for now.
                        tag_line = lines[3].replace("\n", "")
                        desc_line = lines[4].replace("\n", "")

                        tag = tag_line.split(":")[1].strip()
                        desc = desc_line.split(":")[1].strip()

                        if tag != "" and desc != "":
                            enc_str = day_path + "^&*" + tag + "^&*" + desc + "\n"

                            if tag in tag_dict.keys():
                                tag_dict[tag].append(enc_str)
                            else:
                                tag_dict[tag] = [enc_str]

    # Now write back all the modified dicts to files
    for tag in tag_dict.keys():
        path = os.path.join(".diary/tags", tag + ".txt")

        with open(path, "w") as file:
            file.writelines(tag_dict[tag])

    # Print when was it last updated
    with open(".diary/date.txt", "r") as file:
        data = file.readlines()
    date = data[1]
    prRed(f"Update Completed. Last updated on {date}")

def generate_text(date: str, day: int, file_location: str=None)->str:
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

    if file_location is None:
        string = material.replace("DATE", date)
        string = string.replace("DAY", str(days[day]))

    else:
        with open(file_location, "r") as file:
            material = file.read()
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


def create_files(year, month, file_location=None, **kwargs):
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
        file_location: str
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
                        file_str = generate_text(date, i, file_location)
                        file_path = os.path.join(month_path, week_folders[w], date+".md")
                        if f"{date}.md" in os.listdir(os.path.join(month_path, week_folders[w])):
                            raise Exception("File already exists. Continuing will cause rewriting every file. To rewrite everything use `diary clean` in the directory")
                        with open(file_path, "w") as file:
                            file.write(file_str)
                else:
                    if date != 0:
                        date = f"{date}-{months[month]}-{year}"
                        file_str = generate_text(date, i, file_location)
                        file_path = os.path.join(month_path, week_folders[w], date+".md")
                        if f"{date}.md" in os.listdir(os.path.join(month_path, week_folders[w])):
                            raise Exception("File already exists. Continuing will cause rewriting every file. To rewrite everything use `diary clean` in the directory")
                        with open(file_path, "w") as file:
                            file.write(file_str)
    else:
        raise Exception(".diary folder not found. Did you initialise the diary?")

def get_list_tag(tag):
    # Gets the list of all the entires with a particular tag
    tags = os.listdir(".diary/tags")
    tags = [t.replace(".txt", "") for t in tags]

    if tag == "none":
        # Just list the available tags
        prCyan("The list of all available tags: ")
        for tag_ in tags:
            prGreen("- " + tag_)
        print()
        prCyan("To get the list of each tag", end="")
            
    else:
        if tag not in tags:
            prRed("Did not find the listed tag", end="")
            prCyan(f"{tag}")
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