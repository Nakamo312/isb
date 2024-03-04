from PyQt5.QtWidgets import (QApplication)
from typing import List

from lab_1.user_interface.client import Client


class App(QApplication):

    def __init__(self, argv: List[str]):
        super().__init__(argv)
        self.window = None

    def run(self):
        self.window = Client()
        self.exec()
