import os

from PyQt5 import QtCore
from dotenv import load_dotenv
from PyQt5.QtWidgets import (QWidget,
                             QHBoxLayout, QVBoxLayout,
                             QPushButton,
                             QFileDialog,
                             QTableWidget, QTableWidgetItem,
                             QHeaderView, QTextEdit, QLabel, QLineEdit, QDialog, QCheckBox)

from cryptography.Decoder import Decoder
from cryptography.alphabet import Alphabet

from utils.fetch_data import read_from_txt, json_read, json_write, write_to_txt

load_dotenv()
char_freq = json_read(os.path.join("out", "ru.json"))


class NumberInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сaesar key")
        label = QLabel("Enter key:")
        self.line_edit = QLineEdit()
        self.english_checkbox = QCheckBox("ENG")
        self.russian_checkbox = QCheckBox("RU")

        self.button = QPushButton("OK")
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.english_checkbox)
        layout.addWidget(self.russian_checkbox)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.on_button_clicked)
        self.setLayout(layout)

    def on_button_clicked(self):
        number = int(self.line_edit.text())
        lng = "eng"
        if self.russian_checkbox.isChecked():
            lng = "ru"
        self.close()
        return number


class Client(QWidget):
    """
    This is a class designed as a QT window for interact actions for encode and decode text
    """

    def __init__(self):
        super().__init__()
        self.decoder = None
        self.data = None
        self.key = None
        self.alphabet = None
        self.ru_alphabet = Alphabet(None, **char_freq)
        self.set_appears()
        self.initUI()
        self.connects()
        self.show()

    def set_appears(self):
        """
        this method initializes the application window settings
        """
        self.setWindowTitle(os.getenv("TITLE"))
        self.resize((int(os.getenv("WIDTH"))), int(os.getenv("HEIGHT")))
        self.move(int(os.getenv("X_OFF")), int(os.getenv("Y_OFF")))

    def initUI(self):
        """
        this method initializes all Qt widgets used in the application window
        """
        self.open_btn = QPushButton(os.getenv("BUTTON_OPEN"))
        self.save_btn = QPushButton(os.getenv("BUTTON_SAVE"))
        self.replace_btn = QPushButton(os.getenv("BUTTON_REPLACE"))
        self.text = QTextEdit()
        self.result_text = QTextEdit()
        self.caesars_cipher_btn = QPushButton(os.getenv("BUTTON_CIPHER"))
        self.table = QTableWidget(1, 2, self)
        self.table.setHorizontalHeaderLabels([os.getenv("COLUMN_1"), os.getenv("COLUMN_2")])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.table2 = QTableWidget(1, 2, self)
        self.table2.setHorizontalHeaderLabels([os.getenv("COLUMN_1"), os.getenv("COLUMN_2")])
        self.table2.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.lv1 = QVBoxLayout()
        self.lv2 = QVBoxLayout()

        self.lh1 = QHBoxLayout()
        self.lh2 = QHBoxLayout()
        self.lh3 = QHBoxLayout()
        self.lh4 = QHBoxLayout()
        self.lh4.addWidget(self.replace_btn)
        self.lh4.addWidget(self.caesars_cipher_btn)
        self.lv1.addWidget(self.open_btn, alignment=QtCore.Qt.AlignTop)
        self.lv1.addWidget(self.save_btn, alignment=QtCore.Qt.AlignTop)
        self.lh3.addWidget(self.text)
        self.lh3.addWidget(self.result_text)
        self.lv2.addLayout(self.lh3)
        self.lh2.addWidget(self.table)
        self.lh2.addWidget(self.table2)
        self.lv2.addLayout(self.lh2)
        self.lv2.addLayout(self.lh4)
        self.lh1.addLayout(self.lv1)
        self.lh1.addLayout(self.lv2)

        self.setLayout(self.lh1)
        self.fill_ru_table()

    def connects(self):
        """
        this method slots for signals are declared
        """
        self.open_btn.clicked.connect(self.open)
        self.replace_btn.clicked.connect(self.replace)
        self.save_btn.clicked.connect(self.save_data)
        self.caesars_cipher_btn.clicked.connect(self.encode)

    def open(self):
        """this method calls a file dialog to select the text file,\n
           and creates an instance of the "Decoder" class based on it
        """
        path, _ = QFileDialog.getOpenFileName()
        if path:
            self.data = read_from_txt(path)
            self.text.setPlainText(self.data)

            self.alphabet = Alphabet(self.data)
            self.decoder = Decoder(self.data,self.alphabet, self.ru_alphabet)
            self.fill_custom_table()


    def replace(self):
        """
        Replaces selected characters in text
        """
        selected_row1 = self.table.currentRow()
        selected_column1 = self.table.currentColumn()
        selected_row2 = self.table2.currentRow()
        selected_column2 = self.table2.currentColumn()

        sym1 = self.table.item(selected_row1, selected_column1).text()
        sym2 = self.table2.item(selected_row2, selected_column2).text()

        table = [(sym1, sym2)]
        self.result_text.setText(self.decoder.decode(table))

    def fill_custom_table(self):
        """
        Fills the table with symbols frequencies
        """
        self.table.setRowCount(len(self.alphabet.char_freq))
        for index, item in enumerate(self.alphabet.sorted_set()):
            self.table.setItem(index, 0, QTableWidgetItem(item[0]))
            self.table.setItem(index, 1, QTableWidgetItem(str(item[1])))

    def fill_ru_table(self):
        """
        Fills the table with ru symbols frequencies
        """
        self.table2.setRowCount(len(self.ru_alphabet.char_freq))
        for index, item in enumerate(self.ru_alphabet.sorted_set()):
            self.table2.setItem(index, 0, QTableWidgetItem(item[0]))
            self.table2.setItem(index, 1, QTableWidgetItem(str(item[1])))

    def save_data(self):
        """
        Saves ciphertext and key to files
        """
        path, _ = QFileDialog.getSaveFileName(caption="Save encoded text")
        write_to_txt(self.result_text.toPlainText(), path)

        path, _ = QFileDialog.getSaveFileName(caption="Save key")
        json_write(self.decoder.get_key(), path)

    def encode(self):
        """
        Encrypts text using the Caesar algorithm
        """
        dialog = NumberInputDialog()
        key = dialog.exec_()
        self.decoder = Decoder(self.text.toPlainText().lower())
        self.result_text.setText(self.decoder.caesars_cipher(5, lng="ru"))
