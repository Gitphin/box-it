import json
import os
import pathlib
import shutil


class Config:
    def __init__(
        self,
        ext_path="types_config.json",
        pref_path="pref_config.json",
        main_path="main_path_config.json",
        debug=True,
    ):
        # Prints outputs to console, set to false if you do not like this
        self.debug = debug
        # Do not change or modify these paths
        self.ext_path = ext_path
        self.pref_path = pref_path
        self.main_path = main_path
        # Default vals, can add categories or extensions here and the .json file
        # You may need to delete the types_config.json file if you change via this file
        self.file_extensions = {
            "Images": ["jpg", "jpeg", "png", "gif", "bmp", "svg", "tiff", "webp"],
            "Videos": ["mp4", "mkv", "mov", "avi", "flv", "wmv"],
            "Coding": [
                "py",
                "js",
                "html",
                "css",
                "cpp",
                "java",
                "rs",
                "c",
                "md",
                "jsx",
                "sh",
                "json",
                "cs",
                "ml",
                "lua",
                "asm",
                "rb",
                "php",
                "ts",
            ],
            "Documents": [
                "pdf",
                "text",
                "doc",
                "docx",
                "ppt",
                "pptx",
                "plain",
                "xls",
                "xed",
                "xlsx",
                "txt",
                "odt",
            ],
            "Misc": [],
        }

        self.pref = {
            "YEAR": True,
            "CATEGORY": True,
            "TYPES": True,
            "TAG": "-=-",
            "NAME": "BoxIt",
            "MAIN": "Main",
        }

        self.path = {"PATH": pathlib.Path.home() / "Desktop"}
        # Init configs
        self.name = self.pref["NAME"]
        self.main_folder_path = self.path["PATH"]
        self.tag = self.pref["TAG"]
        self.main = self.pref["MAIN"]
        self.year = self.pref["YEAR"]
        self.types = self.pref["TYPES"]
        self.category = self.pref["CATEGORY"]

    def update_main_path_hash(self):
        """Updates the main path hash JSON"""
        try:
            # Convert path to string
            path_dict = {k: str(v) for k, v in self.path.items()}
            with open(self.main_path, "w") as json_file:
                json.dump(path_dict, json_file, indent=4)
        except Exception as e:
            print(f"Could not write to file {self.main_path}: {e}")
            return -1

    def load_main_path_hash(self):
        """Loads in main path hash if exists"""
        if os.path.exists(self.main_path):
            try:
                with open(self.main_path, "r") as json_file:
                    path_dict = json.load(json_file)
                    # Convert string back to path
                    self.path = {k: pathlib.Path(v) for k, v in path_dict.items()}
                    self.main_folder_path = self.path["PATH"]
                    if self.debug:
                        print(f"Loaded in user path: {(self.path['PATH'])}")
            except Exception as e:
                print(f"Could not load preferences from {self.main_path}: {e}")
                return -1
        else:
            if self.debug:
                print("Loaded default path in")

    def update_pref_hash(self):
        """Updates the preference hash JSON"""
        try:
            with open(self.pref_path, "w") as json_file:
                json.dump(self.pref, json_file, indent=4)
        except Exception as e:
            print(f"Could not write to file {self.pref_path}: {e}")
            return -1

    def load_pref_hash(self):
        """Loads in pref hash if exists"""
        if os.path.exists(self.pref_path):
            try:
                with open(self.pref_path, "r") as json_file:
                    self.pref = json.load(json_file)
                    self.name = self.pref["NAME"]
                    self.tag = self.pref["TAG"]
                    self.main = self.pref["MAIN"]
                    self.year = self.pref["YEAR"]
                    self.types = self.pref["TYPES"]
                    self.category = self.pref["CATEGORY"]
                    if self.debug:
                        print("Loaded in user preferences")
            except Exception as e:
                print(f"Could not load preferences from {self.pref_path}: {e}")
                return -1
        else:
            if self.debug:
                print("Loaded default preferences in")

    def update_ext_hash(self):
        """Refresh current extension hash"""
        try:
            with open(self.ext_path, "w") as json_file:
                json.dump(self.file_extensions, json_file, indent=4)
        except Exception as e:
            print(f"Could not write to file {self.ext_path}: {e}")
            return -1

    def load_ext_hash(self):
        """Load ext hash"""
        if os.path.exists(self.ext_path):
            try:
                with open(self.ext_path, "r") as json_file:
                    self.file_extensions = json.load(json_file)
                    if self.debug:
                        print(f"Loaded in user type extension config")
            except Exception as e:
                print(f"Could not load types from {self.ext_path}: {e}")
                return -1
        else:
            if self.debug:
                print(f"Loaded default extensions in")

    def update_path(self, path):
        """Updates path of wrapper folder, takes in PathLib"""
        new_path = path / self.name
        old_path = self.main_folder_path / self.name
        if new_path == self.main_folder_path:
            print("Cannot be the same path")
            return -1
        if self.name:
            if os.path.exists(new_path):
                print(f"Destination path '{new_path}' already exists!")
                return -1
            try:
                shutil.copytree(old_path, new_path)
                if self.debug:
                    print(f"Copied folder from {old_path} to {new_path}")
                shutil.rmtree(old_path)
                if self.debug:
                    print(f"Removed old path: {old_path}")
                self.path["PATH"] = path
                self.main_folder_path = path
                if self.debug:
                    print(f"Changed main folder path to {new_path}")
                self.update_main_path_hash()
            except Exception as e:
                print(f"Error copying or removing the directory: {e}")
                return -1
        else:
            print("Must have a name for the folder")
            return -1

    def update_name(self, new_name):
        """Updates name of wrapper folder"""

        if not new_name.strip():
            print("Name cannot be empty!")
            return -1

        new_path = self.main_folder_path / new_name
        old_path = self.main_folder_path / self.name

        if new_path == old_path:
            print("Cannot be the same path")
            return -1

        if os.path.exists(new_path):
            print(f"Destination path '{new_name}' already exists!")
            return -1

        try:
            shutil.copytree(old_path, new_path)
            if self.debug:
                print(f"Copied folder from {old_path} to {new_path}")
            shutil.rmtree(old_path)
            if self.debug:
                print(f"Removed old folder: {old_path}")
            self.pref["NAME"] = new_name
            self.name = new_name
            if self.debug:
                print(f"Changed name of folder to {new_path}")
            self.update_pref_hash()
        except Exception as e:
            print(f"Error renaming folder from {old_path} to {new_path}: {e}")
            return -1

    def update_main(self, new_main):
        """Updates main folder name"""
        if not new_main.strip():
            print("Main folder name cannot be empty!")
            return -1

        new_path = self.main_folder_path / self.name / new_main
        old_path = self.main_folder_path / self.name / self.main

        if new_path == old_path:
            print("Cannot be the same path")
            return -1

        if os.path.exists(new_path):
            print(f"Destination path '{new_main}' already exists!")
            return -1

        try:
            shutil.copytree(old_path, new_path)
            if self.debug:
                print(f"Copied folder from {old_path} to {new_path}")
            shutil.rmtree(old_path)
            if self.debug:
                print(f"Removed old folder: {old_path}")
            self.pref["MAIN"] = new_main
            self.main = new_main
            if self.debug:
                print(f"Changed main folder name to {new_path}")
            self.update_pref_hash()

        except Exception as e:
            print(f"Error renaming main folder from {old_path} to {new_path}: {e}")
            return -1

    def update_tag(self, new):
        """Updates tag indicator"""
        self.pref["TAG"] = new
        self.tag = new
        self.update_pref_hash()
        if self.debug:
            print(f"Updated filter tag to {self.tag}")

    def update_years(self, state):
        """Updates toggle filters"""
        self.pref["YEAR"] = state
        self.year = state
        self.update_pref_hash()
        if self.debug:
            print(f"Updated displaying years to {self.year}")

    def update_cat(self, state):
        """Updates toggle filters"""
        self.pref["CATEGORY"] = state
        self.category = state
        self.update_pref_hash()
        if self.debug:
            print(f"Updated displaying categories to {self.category}")

    def update_types(self, state):
        """Updates toggle filters"""
        self.pref["TYPES"] = state
        self.types = state
        self.update_pref_hash()
        if self.debug:
            print(f"Updated displaying types to {self.types}")

    def new_category_type(self, name, exts):
        """Add new category/folder"""
        if name in self.file_extensions:
            print(f"Category '{name}' already exists!")
        else:
            self.file_extensions[name] = []
            self.file_extensions[name].extend(
                [ext for ext in exts if ext not in self.file_extensions[name]]
            )
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
            self.file_extensions[name].extend(
                [ext for ext in exts if ext not in self.file_extensions[name]]
            )
            self.update_ext_hash()

    def del_exts(self, name, exts):
        """Filter out/delete extensions in a category"""
        if name not in self.file_extensions:
            print(f"Category '{name}' does not exist!")
        else:
            self.file_extensions[name] = [
                ext for ext in self.file_extensions[name] if ext not in exts
            ]
            self.update_ext_hash()
