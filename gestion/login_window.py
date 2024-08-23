# ui_components.py

import sys
import mysql.connector
from main_window import MainWindow
from add_client_window import AddClientWindow
from add_product_window import AddProductWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QSizePolicy, QHeaderView

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()

        self.user_label = QLabel('Usuario:')
        self.user_entry = QLineEdit()
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_entry)

        self.pass_label = QLabel('Contraseña:')
        self.pass_entry = QLineEdit()
        self.pass_entry.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_label)
        layout.addWidget(self.pass_entry)

        self.login_button = QPushButton('Ingresar')
        self.login_button.setObjectName('add_button')
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        if self.user_entry.text() == 'admin' and self.pass_entry.text() == 'admin':
            self.close()
            self.main_window = MainWindow()
            self.main_window.show()
        else:
            QMessageBox.critical(self, 'Error de autenticación', 'Usuario o contraseña incorrectos')

