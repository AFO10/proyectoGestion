from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
import mysql.connector
import sys

class AgregarProducto(QDialog):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.db_connection = db_connection
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Agregar producto a la canasta')
        self.setGeometry(150, 150, 400, 300)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.cantidad_input = QLineEdit()

        layout.addRow(QLabel('Nombre:'), self.name_input)
        layout.addRow(QLabel('Cantidad:'), self.cantidad_input)

        save_button = QPushButton('Guardar')
        save_button.clicked.connect(self.save_client)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_client(self):
        name = self.name_input.text()
        lastname = self.lastname_input.text()
        dni = self.dni_input.text()
        phone = self.phone_input.text()

        if not (name and lastname and dni and phone):
            QMessageBox.warning(self, 'Advertencia', 'Todos los campos deben ser completados.')
            return

        cursor = self.db_connection.cursor()
        query = "INSERT INTO Cliente (Nombre, Apellido, DNI, Telefono) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, lastname, dni, phone))
        self.db_connection.commit()
        cursor.close()

        QMessageBox.information(self, 'Éxito', 'Cliente agregado exitosamente.')
        self.accept()  # Cierra el diálogo y regresa a la ventana principal