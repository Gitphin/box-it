import json
import os
import pathlib

class Config:
    def __init__(self, ext_path='types_config.json',):
        self.ext_path = ext_path
        # Init file extensions and tags

        self.file_extensions = {
            "Images": ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'tiff'],
            "Videos": ['mp4', 'mkv', 'mov', 'avi', 'flv', 'wmv'],
            "Coding": ['py', 'js', 'html', 'css', 'cpp', 'java', 'cs', 'rb', 'php', 'ts'],
            "Documents": ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt', 'odt'],
            "Misc": []
        }

        self.pref = {
            "YEAR": True,
            "CATEGORY": True,
            "TYPES": True,
            "TAG": "-=-",
            "NAME": "SortedFolder",
            "MAIN": "Main",
        }
        self.name = self.pref["NAME"]
        # WILL HAVE TO UPDATE THIS LATER
        self.main_folder_path = pathlib.Path.home() / 'Desktop' / 'Things' / self.name
        self.tag = self.pref["TAG"]
        self.main = self.pref["MAIN"]
        self.year = self.pref["YEAR"]
        self.types = self.pref["TYPES"]
        self.category = self.pref["CATEGORY"]

    def update_name(self, new):
        """Updates what wrapper folder is called"""
        os.rename(self.main_folder_path, self.main_folder_path / pathlib.Path.home() / 'Desktop' / 'Things' / new )
        self.pref["NAME"] = new
        self.name = new

    def update_main(self, new):
        """Updates main folder name"""
        os.rename(self.main_folder_path / self.main, self.main_folder_path / new)
        self.pref["MAIN"] = new
        self.main = new

    def update_tag(self, new):
        """Updates tag indicator"""
        self.pref["TAG"] = new
        self.tag = new
    
    def update_toggle(self, t):
        """Updates toggle filters"""
        self.pref[t] = False if self.pref[t] else True
        self.t = False if self.t else True
        
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

    def new_category_type(self, name, exts):
        """Add new category/folder"""
        if name in self.file_extensions:
            print(f"Category '{name}' already exists!")
        else:
            self.file_extensions[name] = []
            self.file_extensions[name].extend([ext for ext in exts if ext not in self.file_extensions[name]])
            self.update_ext_hash()

    def del_category_type(self, name):
        """Delete category and exts"""
        if name not in self.file_extensions:
            print(f"Category '{name}' does not exist!")
        else:
            del self.file_extensions[name]
            self.update_ext_hash()

    def rename_category_type(self, name, new):
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




