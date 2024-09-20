
import sys
from PyQt5.QtWidgets import QApplication
from QTApplication.app import MultiProccesTaskExecutor


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MultiProccesTaskExecutor()
    window.show()
    sys.exit(app.exec_())

