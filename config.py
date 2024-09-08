import json
import os
import pathlib

class Config:
    def __init__(self, ext_path='types_config.json', name_for_folder="SortedFolder"):
        self.ext_path = ext_path
        self.name_for_folder = name_for_folder
        self.main_folder_path = pathlib.Path.home() / 'Desktop' / 'Things' / self.name_for_folder

        # Init file extensions
        self.file_extensions = {
            "Images": ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'tiff'],
            "Videos": ['mp4', 'mkv', 'mov', 'avi', 'flv', 'wmv'],
            "Coding": ['py', 'js', 'html', 'css', 'cpp', 'java', 'cs', 'rb', 'php', 'ts'],
            "Documents": ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt', 'odt'],
            "Misc": []
        }

    def update_name(self, new):
        self.name_for_folder = new

    def update_ext_hash(self):
        """Refresh current extension hash"""
        try:
            with open(self.ext_path, 'w') as json_file:
                json.dump(self.file_extensions, json_file, indent=4)
        except Exception as e:
            print(f"Could not write to file {self.ext_path}: {e}")

    def load_ext_hash(self):
        """Load ext hash"""
        if os.path.exists(self.ext_path):
            try:
                with open(self.ext_path, 'r') as json_file:
                    self.file_extensions = json.load(json_file)
            except Exception as e:
                print(f"Could not load types from {self.ext_path}: {e}")
        else:
            print(f"Loaded default extensions in")

    def new_folder_type(self, name, exts):
        """Add new category/folder"""
        if name in self.file_extensions:
            print(f"Category '{name}' already exists!")
        else:
            self.file_extensions[name] = []
            self.file_extensions[name].extend([ext for ext in exts if ext not in self.file_extensions[name]])
            self.update_ext_hash()

    def del_folder_type(self, name):
        """Delete category and exts"""
        if name not in self.file_extensions:
            print(f"Category '{name}' does not exist!")
        else:
            del self.file_extensions[name]
            self.update_ext_hash()

    def rename_folder_type(self, name, new):
        """Rename category by replacing old with a new one"""
        if new in self.file_extensions:
            print(f"Category '{name}' already exists!")
        else:
            self.file_extensions[new] = self.file_extensions[name]
            del self.file_extensions[name]
            self.update_ext_hash()

    def add_exts(self, name, exts):
        """Add extensions to a category"""
        if name not in self.file_extensions:
            print(f"Category '{name}' does not exist!")
        else:
            self.file_extensions[name].extend([ext for ext in exts if ext not in self.file_extensions[name]])
            self.update_ext_hash()

    def del_exts(self, name, exts):
        """Filter out/delete extensions in a category"""
        if name not in self.file_extensions:
            print(f"Category '{name}' does not exist!")
        else:
            self.file_extensions[name] = [ext for ext in self.file_extensions[name] if ext not in exts]
            self.update_ext_hash()




