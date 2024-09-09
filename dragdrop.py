import os
import pathlib
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QLabel, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget)

import box_it_script
from settings import SettingsWindow


class DragDropWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config

        self.setWindowTitle("BoxIt")
        self.setGeometry(100, 100, 500, 400)
        self.setWindowIcon(QIcon("icons/main-icon.svg"))
        self.label = QLabel("Drag a file or folder here", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { border: 2px dashed gray; }")

        # Settings button
        self.settings_button = QPushButton("Settings", self)
        self.settings_button.clicked.connect(self.open_settings)

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.label)
        layout.addWidget(self.settings_button)
        self.setCentralWidget(central_widget)

        # Enable drag/drop
        self.setAcceptDrops(True)

    def open_settings(self):
        """Open the settings dialogue window"""
        settings_window = SettingsWindow(self.config, self)
        settings_window.exec_()

    def dragEnterEvent(self, event):
        """drag event override"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    # Override the dropEvent to handle file or folder drop
    def dropEvent(self, event):
        """drop override, handle"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                file_url = url.toLocalFile()
                path = pathlib.Path(file_url)
                if path.is_dir():
                    self.handle_folder_drop(path)
                elif path.is_file():
                    box_it_script.handle_file_drop(path)
                    self.label.setText(f"File dropped: {path}")
                else:
                    self.label.setText("Unsupported file type or empty drop")

    def handle_folder_drop(self, folder_path):
        """Process all files in the dropped folder."""
        for item in folder_path.iterdir():
            if item.is_file():
                box_it_script.handle_file_drop(item)
        self.label.setText(f"Folder dropped and processed: {folder_path}")
