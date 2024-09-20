from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QSpinBox,
    QWidget
)


class CountSelector(QDialog):
    """
    A dialog for selecting a count or range of counts.
    """

    def __init__(self, caption: str, ranged: bool = False, parent: QWidget =None):
        """
        Initializes the dialog.

        Args:
            caption (str): The title of the dialog.
            ranged (bool): Whether to select a range of counts (True) or a single count (False).
            parent (QWidget): The parent widget, if any.
        """
        super().__init__(parent)
        self.ranged = ranged
        self.setWindowTitle(caption)

        if ranged:
            # Create widgets for ranged count selection
            self.min_label = QLabel("Min count:")
            self.min_spin_box = QSpinBox()
            self.min_spin_box.setMinimum(1)
            self.min_spin_box.setMaximum(100)
            self.min_spin_box.setValue(1)

            self.max_label = QLabel("Max count:")
            self.max_spin_box = QSpinBox()
            self.max_spin_box.setMinimum(1)
            self.max_spin_box.setMaximum(100)
            self.max_spin_box.setValue(10)

            self.ok_button = QPushButton("OK")
            self.ok_button.clicked.connect(self.accept)
            self.cancel_button = QPushButton("Cancel")
            self.cancel_button.clicked.connect(self.reject)

            layout = QVBoxLayout()
            layout2 = QHBoxLayout()

            layout2.addWidget(self.ok_button)
            layout2.addWidget(self.cancel_button)

            layout.addWidget(self.min_label)
            layout.addWidget(self.min_spin_box)
            layout.addWidget(self.max_label)
            layout.addWidget(self.max_spin_box)
            layout.addWidget(self.ok_button)
            layout.addLayout(layout2)
            self.setLayout(layout)
        else:
            # Create widgets for single count selection
            self.min_label = QLabel("count:")
            self.min_spin_box = QSpinBox()
            self.min_spin_box.setMinimum(1)
            self.min_spin_box.setMaximum(100)
            self.min_spin_box.setValue(1)

            self.ok_button = QPushButton("OK")
            self.ok_button.clicked.connect(self.accept)
            self.cancel_button = QPushButton("Cancel")
            self.cancel_button.clicked.connect(self.reject)

            layout = QVBoxLayout()
            layout2 = QHBoxLayout()

            layout2.addWidget(self.ok_button)
            layout2.addWidget(self.cancel_button)

            layout.addWidget(self.min_label)
            layout.addWidget(self.min_spin_box)
            layout.addWidget(self.ok_button)
            layout.addLayout(layout2)
            self.setLayout(layout)

    def get_min_count(self):
        """
        Returns the minimum count selected by the user.
        """
        return self.min_spin_box.value()

    def get_max_count(self):
        """
        Returns the maximum count selected by the user.

        Returns:
            The maximum count if ranged is True, otherwise the minimum count. (int)
        """
        if self.ranged:
            return self.max_spin_box.value()
        else:
            return self.min_spin_box.value()
