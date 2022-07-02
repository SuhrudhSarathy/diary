# Diary
A command line tool to imitate your Research Diary.

## Installation
1. Clone this repository
2. Add the following lines to your .bashrc or .zshrc
```bash
export DIARY_PATH=<path_to_cloned_folder>
alias diary="python $DIARY_PATH/diary/main.py"
```
- If you are using a linux system, use `python3` instead of `python` in the above command.
3. You can now use the diary tools using the keyword `diary`

## Usage
1. To initialise the a repository as a diary
```bash
diary init
```
2. To create a new diary entry for a month and a year (Eg. Jul 2022)
```bash
diary new -m Jul -y 2022
```
This creates a folder with weeks and a defualt markdown file for each day. To generate a the markdown file with any custom file, you can pass the file path as an optional argument. Eg:
```bash
diary new -m Jul -y 2022 -f experiment.md
```
The custom markdown file should contain the following metadata (YAML format) for proper functioning. The strings `DATE` and `DAY` will be formatted when new diary entries are created.
```yaml
---
date: DATE
day: DAY
tag:
description:
---
```
3. Each day is a diary entry. Each diary entry should contain a tag and a description. This helps in searching and updating.

## Additional features
1. For more information about the tool, use `help`
```
diary --help
```
2. To get an explanation for a tool, use `explain`
```
diary --explain
```

## Wiki
Take a look at the sample usage in the [Wiki](https://github.com/SuhrudhSarathy/diary/wiki)