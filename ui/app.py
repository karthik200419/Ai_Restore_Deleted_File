import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QMessageBox, QFileDialog
)
from PyQt5.QtCore import QThread, pyqtSignal
from scanner.disk_scanner import DiskScanner
from reconstructor import ImageReconstructor, VideoReconstructor, TextReconstructor
from ui.components import create_file_list_widget, create_button, create_preview_label, update_preview
from utils import is_admin, to_raw_path, ensure_dir


# -------------------------
# Worker for scanning drive
# -------------------------
class ScanWorker(QThread):
    finished = pyqtSignal(list, str)  # files, error message

    def __init__(self, drive_path):
        super().__init__()
        self.drive_path = drive_path

    def run(self):
        try:
            scanner = DiskScanner(self.drive_path)
            files = scanner.scan_deleted_files()
            self.finished.emit(files, "")
        except Exception as e:
            self.finished.emit([], str(e))


# ------------------------------
# Worker for reconstructing file
# ------------------------------
class ReconstructWorker(QThread):
    finished = pyqtSignal(str, str)  # output path, error message

    def __init__(self, file_data, scanner):
        super().__init__()
        self.file_data = file_data
        self.scanner = scanner

    def run(self):
        try:
            recovered_path = self.scanner.recover_file(self.file_data['inode'])
            if not recovered_path:
                self.finished.emit("", "Failed to recover file")
                return

            ext = os.path.splitext(self.file_data['name'])[1].lower()
            output_path = None
            reconstructor = None

            if ext in [".png", ".jpg", ".jpeg", ".bmp"]:
                reconstructor = ImageReconstructor()
                output_path = "reconstructed_files/reconstructed_img.png"
                reconstructor.reconstruct(recovered_path, "mask.png", output_path)

            elif ext in [".txt", ".doc", ".docx"]:
                reconstructor = TextReconstructor()
                output_path = "reconstructed_files/reconstructed_text.txt"
                reconstructor.reconstruct(recovered_path, output_path)

            elif ext in [".mp4", ".avi", ".mov", ".mkv"]:
                reconstructor = VideoReconstructor()
                output_path = "reconstructed_files/reconstructed_video.mp4"
                reconstructor.reconstruct(recovered_path, output_path)

            self.finished.emit(output_path, "")
        except Exception as e:
            self.finished.emit("", str(e))


# -----------------
# Main UI
# -----------------
class AI_Restore_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Restore")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Buttons
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

        # Ensure necessary folders exist
        ensure_dir("recovered_files")
        ensure_dir("reconstructed_files")

    # -----------------
    # Select drive
    # -----------------
    def select_drive(self):
        if not is_admin():
            QMessageBox.critical(self, "Error", "You must run this program as administrator.")
            return

        drive_path = QFileDialog.getExistingDirectory(self, "Select Drive")
        if not drive_path:
            return

        drive_path = to_raw_path(drive_path)

        # run in background
        self.scan_worker = ScanWorker(drive_path)
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.start()

    def on_scan_finished(self, files, error):
        if error:
            QMessageBox.critical(self, "Error", f"Failed to scan drive: {error}")
            return

        self.deleted_files = files
        self.file_list.clear()
        for file in self.deleted_files:
            self.file_list.addItem(f"{file['name']} | size: {file['size']} bytes")

    # -----------------
    # Reconstruct file
    # -----------------
    def reconstruct_file(self):
        selected = self.file_list.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "No file selected")
            return

        file_data = self.deleted_files[selected]

        # run in background
        self.reconstruct_worker = ReconstructWorker(file_data, self.scanner)
        self.reconstruct_worker.finished.connect(self.on_reconstruct_finished)
        self.reconstruct_worker.start()

    def on_reconstruct_finished(self, output_path, error):
        if error:
            QMessageBox.critical(self, "Error", error)
            return

        if not output_path:
            QMessageBox.warning(self, "Error", "Reconstruction failed")
            return

        ext = os.path.splitext(output_path)[1].lower()
        if ext in [".png", ".jpg", ".jpeg", ".bmp"]:
            update_preview(self.preview_label, output_path)
        else:
            self.preview_label.setText(f"Reconstructed file saved at: {output_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AI_Restore_UI()
    window.show()
    sys.exit(app.exec_())
