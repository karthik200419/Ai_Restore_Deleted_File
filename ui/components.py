from PyQt5.QtWidgets import QPushButton, QListWidget, QLabel
from PyQt5.QtGui import QPixmap

def create_button(text, callback):
    btn = QPushButton(text)
    btn.clicked.connect(callback)
    return btn

def create_file_list_widget():
    return QListWidget()

def create_preview_label():
    lbl = QLabel("Preview will appear here")
    lbl.setFixedSize(400, 300)
    lbl.setStyleSheet("border: 1px solid black;")
    return lbl

def update_preview(preview_label, file_path):
    pixmap = QPixmap(file_path)
    if not pixmap.isNull():
        preview_label.setPixmap(pixmap.scaled(preview_label.width(), preview_label.height()))
    else:
        preview_label.setText("Preview not available")
