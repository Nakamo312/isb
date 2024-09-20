import logging
import time

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMainWindow,
    QAction,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QDialog
)

from Model.serialize import Serializable
from Model.test_data import TestData
from QTApplication.Widgets.callib_window_widget import CalibWindow
from QTApplication.Widgets.count_selector_widget import CountSelector
from Sevices.file_services.file_handler import FileHandler
from .Sevices.worker_thread import WorkerThread
from .Widgets.data_widget import DataWidget
from .Widgets.dinamic_graph_widget import DynamicGraphWidget
from .Widgets.mode_selector import ModeSelector


class MultiProccesTaskExecutor(QMainWindow):
    """
    Main window for multiprocess task execution.
    """

    def __init__(self):
        super().__init__()

        self.file_handler = FileHandler("", "")

        self.setWindowTitle("Поиск карты")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.indata_widget = DataWidget("Input data") 
        self.outdata_widget = DataWidget("Output data") 
        self.graph_widget = DynamicGraphWidget()
        self.mode_selector = ModeSelector()
        self.start_button = QPushButton("")
        self.start_button.setText("Start worker thread")
        self.start_button.clicked.connect(self.start_work)
        self.progress = QLabel("")
        self.progress.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        self.status_label = QLabel("")
        self.results_label = QLabel("")

        group_box = QGroupBox("Speed rate")
        form_layout = QFormLayout()
        form_layout.addRow(self.graph_widget)
        form_layout.addRow(self.progress)
        group_box.setLayout(form_layout)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.indata_widget)
        vlayout.addWidget(self.mode_selector)
        vlayout.addWidget(self.start_button)
        hlayout = QHBoxLayout()
        hlayout.addLayout(vlayout)
        hlayout.addWidget(group_box)

        layout = QVBoxLayout()
        layout.addLayout(hlayout)

        layout.addWidget(self.status_label)
        layout.addWidget(self.outdata_widget)
        layout.addWidget(self.results_label)

        central_widget.setLayout(layout)
        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)

        self.worker_thread = None

    def open_file(self) -> None:
        """
        Opens a file dialog and loads data into the input widget.
        """
        file_name, _ = QFileDialog.getOpenFileName(
            self, 
            "Open", 
            "", 
            " (*.json);;"
        )
        if file_name:
            self.file_handler.in_path = file_name
            self.indata_widget.update_data(self.file_handler.read()) 

    def save_file(self) -> None:
        """
        Opens a file dialog and saves data to a file.
        """
        file_name, _ = QFileDialog.getSaveFileName(
            self, 
            "Save", 
            "", 
            " (*.json);;"
        )
        if file_name:
            self.file_handler.out_path = file_name
            self.file_handler.write(self.out_data)

    def start_search(self, process_count: int) -> WorkerThread:
        """
        Starts the search process with the specified number of processes.

        Args:
            process_count (int): The number of processes to use.

        Returns:
            The worker thread instance.(WorkerThread)
        """
        try:
            if not isinstance(self.indata_widget.data, Serializable):
                raise ValueError("Incorrect format input file")
            self.worker_thread = WorkerThread(self.indata_widget.data, process_count)
            self.worker_thread.status_signal.connect(self.update_status)
            self.worker_thread.finished_signal.connect(self.finish_search)
            self.worker_thread.iterations_signal.connect(self.update_progress)
            self.worker_thread.out_result_signal.connect(self.update_out_data)
            self.worker_thread.start()

            self.start_button.setEnabled(False)
            return self.worker_thread
        except Exception as e:
            logging.error(f"[CardSearchApp]: Error starting search: {e}")
            self.status_label.setText(f"Error: {e}")

    def update_progress(self, iterations: float, cur_time: float) -> None:
        """
        Updates information in widgets according to current progress

        Args:
            iterations (float): current number of iterations per unit of time.
            cur_time (float):  current time since the task started
        """
        self.graph_widget.xs.append(cur_time)
        self.graph_widget.ys.append(iterations)
        cur_time = time.strftime("%H:%M:%S", time.localtime(cur_time))
        self.progress.setText(f"{iterations}/ms, {cur_time}")

    def update_out_data(self, out_data: Serializable):
        """
        Displays the output of a task in a widget

        Args:
            out_data (Serializable): output data of a current task
        """
        self.outdata_widget.update_data(out_data) 

    def update_status(self, status: str):
        """
        Displays the status of a task in a widget

        Args:
            status (str): status of a current task
        """
        self.progress.setText(status)

    def finish_search(self, test_data: TestData):
        """
        Displays the output test data of a task in a widget
        and and prepares widgets for the next launch

        Args:
            test_data (TestData): output test data of a current task
        """
        self.start_button.setEnabled(True)
        if test_data.succes:
            self.status_label.setText(f"Searching is complete. Total time: {test_data.total_time}.")
        else:
            self.status_label.setText(f"Error during search.")

    def start_work(self):
        """
        Selecting and launch mode before starting work
        """
        mode = self.mode_selector.get_selected_mode()
        match mode:
            case 1:
                self.operation_mode()
            case 2:
                self.calibration_mode()

    def operation_mode(self):
        """
        Launches a single task launch mode with the selected number of processes
        """
        process_count_selector = CountSelector("Process count", ranged=False)
        result = process_count_selector.exec_()
        if result == QDialog.Accepted:
            min_count = process_count_selector.get_min_count()
            self.start_search(min_count)
        else:
            return
    
    def calibration_mode(self):
        """
        Triggers a cascade task launch mode in the selected range
        """
        process_count_selector = CountSelector("Process count", ranged=True)
        result = process_count_selector.exec_()
        if result == QDialog.Accepted:
            min_count = process_count_selector.get_min_count()
            max_count = process_count_selector.get_max_count()
            dialog = CalibWindow(min_count,max_count, self.start_search)
            dialog.exec_()
        else:
            return