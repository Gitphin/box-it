import pathlib
import sys
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

import box_it_script

# DONE WITH HELP OF AI
class DragDropWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("BoxIt")
        self.setGeometry(100, 100, 500, 400)

        # Set up the label to display the file path
        self.label = QLabel("Drag a file or folder here", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { border: 2px dashed gray; }")

        # Set up the central widget with a layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.label)
        self.setCentralWidget(central_widget)

        # Enable drag and drop for the window
        self.setAcceptDrops(True)

    # Override the dragEnterEvent to accept the drag
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    # Override the dropEvent to handle file or folder drop
    def dropEvent(self, event):
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

# Set up the application and run the main window
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DragDropWindow()
    window.show()
    sys.exit(app.exec_())
