import datetime
import os
import pathlib
import shutil
import sys

from config import Config

config = Config(debug=True)

#################################################
# BOX-IT MAIN SCRIPT (DOES THE FILE MOVING FUN) #
#################################################


def file_sorting(sort_dir, file_ext):
    """Get file type to store file in proper folder"""
    for k, v in config.file_extensions.items():
        if file_ext in v:
            return sort_dir / k
    return sort_dir / "Misc"


def check_exists(path):
    """Create a folder if path dne."""
    if not path.exists():
        path.mkdir(parents=True)
        if config.debug:
            print(f"Folder created at {path}")


def handle_file_drop(file_path):
    """Handle loading in the file being dropped"""
    file_input = os.path.basename(file_path)

    # Check if file path exists and is a valid file
    if not file_path.exists() or not file_path.is_file():
        print(f"File path '{file_path}' either invalid or DNE")
        sys.exit(1)

    # Loads in configs to apply any changes
    config.load_ext_hash()
    config.load_pref_hash()
    config.load_main_path_hash()

    # Split the name and file extension
    name = pathlib.Path(file_input).stem
    ext = pathlib.Path(file_input).suffix
    get_name = str(name)
    get_ext = str(ext)[1:]

    # Get tag, change file name to remove tag and place in proper folder, and get starting path
    get_tag = get_name.split(config.tag)
    if len(get_tag) >= 2:
        file_input = get_tag[0] + "." + get_ext
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
        type_folder = file_sorting(sort_dir, get_ext.lower())
        sort_dir = type_folder
        check_exists(sort_dir)

    # Gets proper extension folder
    if config.types:
        ext_folder = sort_dir / get_ext.lower()
        sort_dir = ext_folder
        check_exists(sort_dir)

    # Gets proper year folder
    if config.year:
        create_time = file_path.stat().st_ctime
        create_date = str(datetime.datetime.fromtimestamp(create_time))[:4]
        year_folder = sort_dir / create_date
        sort_dir = year_folder
        check_exists(sort_dir)

    # Moves file into final folder
    sort_file_path = sort_dir / file_input
    shutil.move(str(file_path), str(sort_file_path))
    if config.debug:
        print(f"Moved to: {sort_file_path}")
