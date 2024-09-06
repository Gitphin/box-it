import os, datetime
import shutil
import pathlib

name_for_folder = "SortedFolder"

file_input = input("Enter file name & type: ")
# Will have to change file_path from cwd to just wherever file is located when drag and dropped
file_path = os.getcwd() + "/" + file_input

# Get creation date, set to get year
create_time = os.path.getctime(file_path)
create_date = str(datetime.datetime.fromtimestamp(create_time))[:4]

get_ext = os.path.splitext(file_input)
# Check if a folder to store sorted files exists, if not make
sort_dir = pathlib.Path.home() / 'Desktop' / name_for_folder
if not os.path.exists(sort_dir):
    os.mkdir(sort_dir)
# Check if a folder to store specific file type exists, if not make
ext_folder = sort_dir / get_ext[1]
if not os.path.exists(ext_folder):
    os.mkdir(ext_folder)
# Check if a folder to store create date exists, if not make
year_sorted = ext_folder / create_date
if not os.path.exists(year_sorted):
    os.mkdir(year_sorted)
# Moves file to sorted file folder w/ right type
sort_file_path = year_sorted / file_input
shutil.move(file_path, sort_file_path)
