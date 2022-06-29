# Diary
A command line tool to imitate your Research Diary.

## Installation
1. Clone this repository
2. Add the following lines to your .bashrc or .zshrc
```bash
export DIARY_PATH=<path_to_cloned_folder>
alias diary="python $DIARY_PATH/diary/main.py"
```
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
This creates a folder with weeks and subdirectories and a Markdown file for each day.
3. Each day is a diary entry.

## Additional features
1. For more information about the tool, use `help`
```
diary --help
```
2. To get an explanation for a tool, use `explain`
```
diary --explain
```

## TODO
- [ ] Implement Goto functionality
- [ ] Implement searching by tags
- [ ] Pretty print entries with sub directories
- [ ] Proper documentation