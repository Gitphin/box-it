import os, sys
import datetime
import shutil
import pathlib
from config import Config

config = Config()

def file_sorting(file_ext):
    """Get path to store file in proper folder"""
    for k, v in config.file_extensions.items():
        if file_ext in v:
            return sort_dir / k
    return sort_dir / "Misc"

def check_exists(path):
    """Create a folder if path dne."""
    if not path.exists():
        path.mkdir(parents=True)

# Load in saved config for folder grouping/extensions
config.load_ext_hash()

file_input = input("Enter file name with extension: ") 
file_path = pathlib.Path.cwd() / file_input

if not file_path.exists():
    print(file_path)
    sys.exit(1)

# Get year file was created
create_time = file_path.stat().st_ctime
create_date = str(datetime.datetime.fromtimestamp(create_time))[:4]

# Get the proper file extension
get_ext = file_input.split('.')[-1].lower()

# Get starting path
sort_dir = config.main_folder_path
check_exists(sort_dir)

# Get proper folder type, uses helper file_sorting to look through file_extension hash
type_folder = file_sorting(get_ext)
check_exists(type_folder)

# Gets proper extension folder
ext_folder = type_folder / get_ext
check_exists(ext_folder)

# Gets proper year folder
year_folder = ext_folder / create_date
check_exists(year_folder)

# Moves file into final folder
sort_file_path = year_folder / file_input
shutil.move(str(file_path), str(sort_file_path))
print(f"Moved to: {sort_file_path}")

