from PyQt5.QtWidgets import QListWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap


def create_file_list_widget():
    """
    Create a QListWidget for displaying deleted file names.
    """
    file_list = QListWidget()
    file_list.setMinimumHeight(200)
    return file_list


def create_button(label, callback):
    """
    Create a QPushButton with a label and click callback.
    """
    button = QPushButton(label)
    button.clicked.connect(callback)
    return button


def create_preview_label(width=400, height=400):
    """
    Create a QLabel to show reconstructed file previews.
    """
    label = QLabel("Preview will appear here")
    label.setFixedSize(width, height)
    label.setStyleSheet("border: 1px solid black;")
    label.setScaledContents(True)
    return label


def update_preview(label: QLabel, file_path: str):
    """
    Update a QLabel with an image preview.
    """
    pixmap = QPixmap(file_path)
    label.setPixmap(pixmap)
