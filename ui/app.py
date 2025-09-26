import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QMessageBox, QFileDialog
from scanner.disk_scanner import DiskScanner
from reconstructor.image_reconstructor import ImageReconstructor
from ui.components import (
    create_file_list_widget,
    create_button,
    create_preview_label,
    update_preview
)


class AI_Restore_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Restore")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Create UI components
        self.select_drive_button = create_button("Select Drive", self.select_drive)
        self.layout.addWidget(self.select_drive_button)

        self.file_list = create_file_list_widget()
        self.layout.addWidget(self.file_list)

        self.reconstruct_button = create_button("Reconstruct Selected File", self.reconstruct_file)
        self.layout.addWidget(self.reconstruct_button)

        self.preview_label = create_preview_label()
        self.layout.addWidget(self.preview_label)

        self.setLayout(self.layout)

        # Data variables
        self.scanner = None
        self.deleted_files = []

    def select_drive(self):
        drive_path = QFileDialog.getExistingDirectory(self, "Select Drive")
        if not drive_path:
            return

        self.scanner = DiskScanner(drive_path)
        self.deleted_files = self.scanner.scan_deleted_files()

        self.file_list.clear()
        for file in self.deleted_files:
            self.file_list.addItem(f"{file['name']} | size: {file['size']}")

    def reconstruct_file(self):
        selected = self.file_list.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "No file selected")
            return

        file_data = self.deleted_files[selected]
        recovered_path = self.scanner.recover_file(file_data['inode'])
        
        reconstructor = ImageReconstructor()
        reconstructed_path = reconstructor.reconstruct(
            damaged_image_path=recovered_path,
            mask_image_path="mask.png",
            output_path="reconstructed_files/reconstructed_img.png"
        )

        if reconstructed_path:
            update_preview(self.preview_label, reconstructed_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AI_Restore_UI()
    window.show()
    sys.exit(app.exec_())
