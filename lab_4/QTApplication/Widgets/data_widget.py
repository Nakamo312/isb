from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QListWidget,
    QGroupBox,
    QScrollArea,
    QLabel
)

from Model.serialize import Serializable


class DataWidget(QWidget):
    """
    A widget for displaying data in a user-friendly format.
    """

    def __init__(self, caption: str):
        """
        Initializes the data widget.

        Args:
            caption (str): The caption for the widget.
        """
        super().__init__()
        self.data: Serializable = None
        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        group_box = QGroupBox(caption)
        group_box.setLayout(self.form_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(group_box)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area)
        self.setLayout(self.layout)

    def clear(self):
        while self.form_layout.count() > 0:
            item = self.form_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def update_data(self, data: Serializable):
        """
        Updates the data displayed in the widget.

        Args:
            data (Serializable): The new data to display.
        """
        self.data = data
        self.clear()  # Clear existing data before updating

        for key in data.__dict__:
            value = data[key]
            label = QLabel(f"<h3><r>{key}</r></h3>")
            if isinstance(value, str | int | float):
                field = QLabel()
                field.setText(str(value))
            elif isinstance(data[key], list):
                field = QListWidget()
                scroll_area = QScrollArea()
                scroll_area.setWidget(field)
                scroll_area.setWidgetResizable(True)
                for v in value:
                    field.addItem(str(v))

                field = scroll_area
            self.form_layout.addRow(label, field)