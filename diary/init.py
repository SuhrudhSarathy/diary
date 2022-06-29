"""This file will be called when the `diary init` command will be called
On initialisation:
    1. create a .diary folder
"""
import os
import datetime
from create_files import months
from print_color import *

def initialise_diary() :
    pwd = os.getcwd()

    try:
        os.mkdir(os.path.join(pwd, ".diary"))
        os.mkdir(os.path.join(pwd, ".diary", "tags"))
        with open(os.path.join(pwd, ".diary/date.txt"), "w") as file:
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            file.write(dt_string+"\n")
    except FileExistsError:
        with open(os.path.join(pwd, ".diary/date.txt"), "r") as file:
            data = file.readlines()
        date = data[0]
        print(f"Diary already exists. Diary was created on {date}")
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

if __name__ == "__main__":
    update()