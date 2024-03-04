import os
import sys
from typing import List, Set
from functools import partial
from dotenv import load_dotenv
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QHBoxLayout, QVBoxLayout,
                             QPushButton, QLabel,
                             QListWidget, QFileDialog,
                             QTableWidget, QTableWidgetItem,
                             QLayoutItem, QHeaderView, QTextEdit)

from lab_1.cryptography.Decoder import Decoder
from lab_1.cryptography.alphabet import Alphabet, char_freq
from lab_1.utils.fetch_data import read_from_file

load_dotenv()


class Client(QWidget):
    '''This is a class designed as a QT window for interact actions for encode and decode text'''

    def __init__(self):
        super().__init__()
        self.decoder = None
        self.data = None
        self.alphabet = None
        self.ru_alphabet = Alphabet(None, **char_freq)
        self.set_appears()
        self.initUI()
        self.connects()
        self.show()

    def set_appears(self):
        '''this method initializes the application window settings'''
        self.setWindowTitle(os.getenv("TITLE"))
        self.resize((int(os.getenv("WIDTH"))), int(os.getenv("HEIGHT")))
        self.move(int(os.getenv("X_OFF")), int(os.getenv("Y_OFF")))

    def initUI(self):
        '''this method initializes all Qt widgets used in the application window'''
        self.open_btn = QPushButton(os.getenv("BUTTON_OPEN"))
        self.replace_btn = QPushButton(os.getenv("BUTTON_REPLACE"))
        self.text = QTextEdit()
        self.result_text = QTextEdit()

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
        self.lv1.addWidget(self.open_btn)
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
        '''this method slots for signals are declared'''
        self.open_btn.clicked.connect(self.open)
        self.replace_btn.clicked.connect(self.replace)

    def open(self):
        '''this method calls a file dialog to select the working directory,\n
           and creates an instance of the "DataWriteReader" class based on it
        '''
        path, _ = QFileDialog.getOpenFileName()
        if path:
            self.data = read_from_file(path)
            self.text.setPlainText(self.data)

            self.alphabet = Alphabet(self.data)
            self.decoder = Decoder(self.alphabet, self.ru_alphabet, self.data)
            self.fill_custom_table()
            # self.encoder.compare_alphabets()
            # self.result_text.setText(self.encoder.encode())

    def replace(self):
        selected_row1 = self.table.currentRow()
        selected_column1 = self.table.currentColumn()
        selected_row2 = self.table2.currentRow()
        selected_column2 = self.table2.currentColumn()

        sym1 = self.table.item(selected_row1, selected_column1).text()
        sym2 = self.table2.item(selected_row2, selected_column2).text()

        table = [(sym1, sym2)]
        print(table)
        self.result_text.setText(self.decoder.decode(table))

    def fill_custom_table(self):
        self.table.setRowCount(len(self.alphabet.char_freq))
        for index, item in enumerate(self.alphabet.sorted_set()):
            self.table.setItem(index, 0, QTableWidgetItem(item[0]))
            self.table.setItem(index, 1, QTableWidgetItem(str(item[1])))

    def fill_ru_table(self):
        self.table2.setRowCount(len(self.ru_alphabet.char_freq))
        for index, item in enumerate(self.ru_alphabet.sorted_set()):
            self.table2.setItem(index, 0, QTableWidgetItem(item[0]))
            self.table2.setItem(index, 1, QTableWidgetItem(str(item[1])))
