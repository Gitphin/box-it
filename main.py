import sys

from PyQt5.QtWidgets import QApplication

from config import Config
from dragdrop import DragDropWindow


def apply_style(app):
    with open("style.qss", "r") as style_file:
        app.setStyleSheet(style_file.read())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = Config(debug=True)

    apply_style(app)  # Apply the modern style

    window = DragDropWindow(config)
    window.show()

    sys.exit(app.exec_())
