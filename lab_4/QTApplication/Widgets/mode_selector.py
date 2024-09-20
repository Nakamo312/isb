from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
)


class ModeSelector(QWidget):
    """
    A widget for selecting a mode from a set of options.
    """

    def __init__(self, parent=None):
        """
        Initializes the mode selector widget.

        Args:
            parent: The parent widget, if any.
        """
        super().__init__(parent)

        self.mode_label = QLabel("Mode:")

        self.mode_1_radio = QRadioButton("Operating")
        self.mode_2_radio = QRadioButton("Calibration")
        self.mode_1_radio.setChecked(True)  # Default to mode 1

        layout = QVBoxLayout()
        layout.addWidget(self.mode_label)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.mode_1_radio)
        radio_layout.addWidget(self.mode_2_radio)
        layout.addLayout(radio_layout)

        self.setLayout(layout)

    def get_selected_mode(self):
        """
        Returns the currently selected mode.

        Returns:
            1 for "Operating" mode, 2 for "Calibration" mode. (int)
        """
        if self.mode_1_radio.isChecked():
            return 1
        else:
            return 2
    