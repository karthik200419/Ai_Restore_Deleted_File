from ui.app import AI_Restore_UI
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AI_Restore_UI()
    window.show()
    sys.exit(app.exec_())
