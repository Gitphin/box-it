from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QCheckBox, QDialog, QFormLayout,
                             QLineEdit, QPushButton)

class SettingsWindow(QDialog):
    def __init__(self, config, main_window):
        super().__init__()
        self.config = config
        self.main_window = main_window
        self.setWindowIcon(QIcon("icons/main-icon.svg"))

        # Load in configs
        config.load_ext_hash()
        config.load_pref_hash()
        config.load_main_path_hash()

        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 300, 300)

        layout = QFormLayout()

        # Tag
        self.tag_input = QLineEdit(self)
        self.tag_input.setText(config.tag)

        # Years
        self.year_checkbox = QCheckBox(self)
        self.year_checkbox.setChecked(config.pref.get("YEAR", False))

        # Categories
        self.cat_checkbox = QCheckBox(self)
        self.cat_checkbox.setChecked(config.pref.get("CATEGORY", False))

        # Types
        self.types_checkbox = QCheckBox(self)
        self.types_checkbox.setChecked(config.pref.get("TYPES", False))

        # Name of folder
        self.name_input = QLineEdit(self)
        self.name_input.setText(config.pref.get("NAME", ""))

        # Name of main folder
        self.main_input = QLineEdit(self)
        self.main_input.setText(config.pref.get("MAIN", ""))

        # Save button
        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_settings)

        layout.addRow("Update Tag:", self.tag_input)
        layout.addRow("Toggle Year Filter:", self.year_checkbox)
        layout.addRow("Toggle Category Filter:", self.cat_checkbox)
        layout.addRow("Toggle Types Filter:", self.types_checkbox)
        layout.addRow("Update Name:", self.name_input)
        layout.addRow("Update Main Folder:", self.main_input)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_settings(self):
        """Saves settings, checks which changed"""
        new_tag = self.tag_input.text().strip()
        if new_tag != self.config.tag:
            self.config.update_tag(new_tag)

        current_year = self.config.pref.get("YEAR", False)
        if self.year_checkbox.isChecked() != current_year:
            self.config.update_years(self.year_checkbox.isChecked())

        current_cat = self.config.pref.get("CATEGORY", False)
        if self.cat_checkbox.isChecked() != current_cat:
            self.config.update_cat(self.cat_checkbox.isChecked())

        current_types = self.config.pref.get("TYPES", False)
        if self.types_checkbox.isChecked() != current_types:
            self.config.update_types(self.types_checkbox.isChecked())

        new_name = self.name_input.text().strip()
        new_main = self.main_input.text().strip()
        current_name = self.config.pref.get("NAME", "")
        current_main = self.config.pref.get("MAIN", "")
        
        # Ensures that setting a blank folder name is not possible (for pathing issues)
        if new_name and new_name != current_name:
            self.config.update_name(new_name)
        elif not new_name:
            print("Name cannot be empty!")

        if new_main and new_main != current_main:
            self.config.update_main(new_main)
        elif not new_main:
            print("Main folder name cannot be empty!")

        self.close()
