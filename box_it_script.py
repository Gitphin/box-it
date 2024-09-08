import os, sys
import datetime
import shutil
import pathlib
from config import Config

config = Config(debug=True)

def file_sorting(file_ext):
    """Get file type to store file in proper folder"""
    for k, v in config.file_extensions.items():
        if file_ext in v:
            return sort_dir / k
    return sort_dir / "Misc"

def check_exists(path):
    """Create a folder if path dne."""
    if not path.exists():
        path.mkdir(parents=True)

# Load in saved config 
config.load_ext_hash()
config.load_pref_hash()
config.load_main_path_hash()
# config.update_name("Testing")
# config.update_main("Test")
# config.update_path(pathlib.Path.home() / 'Desktop' / 'Things')

# Get user input for file name (WILL CHANGE TO DRAG/DROP"
file_input = input("Enter file name with extension: ") 
file_path = pathlib.Path.cwd() / file_input

# Check if file path exists and is a valid file
if not file_path.exists() or not file_path.is_file():
    print(f"File path '{file_path}' either invalid or DNE")
    sys.exit(1)

# Split the name and file extension
get_name, get_ext = file_input.split('.')

# Get tag (separated by -), change file name to remove tag and place in proper folder, and get starting path
get_tag = get_name.split(config.tag)
if len(get_tag) >= 2:
    file_input = get_tag[0] + '.' + get_ext
    os.rename(file_path, pathlib.Path.cwd() / (file_input))
    file_path = pathlib.Path.cwd() / file_input
    tag_name = get_tag[-1].lower()
    sort_dir = config.main_folder_path / config.name / tag_name
    check_exists(sort_dir)
else:
    sort_dir = config.main_folder_path / config.name / config.main
    check_exists(sort_dir)
    
# Get proper folder type, uses helper file_sorting to look through file_extension hash
if config.category:
    type_folder = file_sorting(get_ext.lower())
    sort_dir = type_folder
    check_exists(sort_dir)

# Gets proper extension folder
if config.types:
    ext_folder = sort_dir / get_ext.lower()
    sort_dir = ext_folder
    check_exists(sort_dir)

# Gets proper year folder
if config.year:
    # Get year file was created
    create_time = file_path.stat().st_ctime
    create_date = str(datetime.datetime.fromtimestamp(create_time))[:4]
    year_folder = sort_dir / create_date
    sort_dir = year_folder
    check_exists(sort_dir)

# Moves file into final folder
sort_file_path = sort_dir / file_input
shutil.move(str(file_path), str(sort_file_path))
print(f"Moved to: {sort_file_path}")

