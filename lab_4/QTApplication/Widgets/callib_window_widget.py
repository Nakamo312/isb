from typing import Callable

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5.QtWidgets import (
    QApplication,
    QAction,
    QFileDialog,
    QListWidget,
    QDialog,
    QGridLayout,
    QSizePolicy,
    QListWidgetItem,
    QMenu
)
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

from Model.test_data import TestData


class CalibWindow(QDialog):
    """
    A dialog for calibrating the performance of a brute-force attack.
    """

    def __init__(self, min_procces_count: int, max_process_count: int, cll_func: Callable):
        """
        Initializes the dialog.

        Args:
            min_procces_count (int): Minimum number of processes to test.
            max_process_count (int): Maximum number of processes to test.
            cll_func (Callable): Callable function to create a worker thread.
        """
        super().__init__()
        self.cll_func = cll_func
        self.min_procces_count = min_procces_count
        self.max_process_count = max_process_count
        self.counter = self.min_procces_count
        self.categories: list = []
        self.hist_data: list = []

        self.setWindowTitle("Test")

        layout = QGridLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget, 2, 0)
        self.list_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas, 2, 1)

        self.setLayout(layout)

        self.start_process()

        self.canvas.setContextMenuPolicy(Qt.CustomContextMenu)
        self.canvas.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self):
        """
        Shows a context menu for saving the chart.
        """
        menu = QMenu(self)
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_chart)
        menu.addAction(save_action)
        menu.exec_(QCursor.pos())

    def start_process(self):
        """
        Starts the process of testing different process counts.
        """
        self.__next_process()
        QApplication.processEvents()

    def __next_process(self, data: TestData = None):
        """
        Runs the next process and updates the UI.

        Args:
            data (TestData): Test data from the previous process, if any.
        """
        if data:
            self.update_histogram(data)
            self.update_list_widget(data)
        if self.counter > self.max_process_count:
            return
        worker = self.cll_func(self.counter)

        worker.finished_signal.connect(self.__next_process)
        self.counter += 1

    def update_histogram(self, data: TestData):
        """
        Updates the histogram with the new data.

        Args:
            data (TestData): Test data to add to the histogram.
        """
        self.hist_data.append(float(data['total_time']))
        self.categories.append(data['process_count'])

        self.figure.clf()
        ax = self.figure.add_subplot(111)

        ax.bar(self.categories, self.hist_data, color="red")
        ax.grid(True)
        ax.set_xlabel("Process count")
        ax.set_ylabel("time")
        self.canvas.draw()

    def update_list_widget(self, data: TestData):
        """
        Updates the list widget with the new data.

        Args:
            data (TestData): Test data to add to the list widget.
        """
        item = QListWidgetItem(f"Process count: {data['process_count']}n Total time: {data['total_time']}n")
        self.list_widget.addItem(item)

    def save_chart(self):
        """
        Saves the chart to a file.
        """
        filename, _ = QFileDialog.getSaveFileName(self, "Save Chart", "", "PNG (*.png);;JPEG (*.jpg);;SVG (*.svg)")
        if filename:
            self.figure.savefig(filename)