# main.py

import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
from main_window import MainWindow
from add_client_window import AddClientWindow
from add_product_window import AddProductWindow

def main():
    app = QApplication(sys.argv)
    # Cargar el archivo QSS
    with open("estilo.qss", "r") as file:
        app.setStyleSheet(file.read())

    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
