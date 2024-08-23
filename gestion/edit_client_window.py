from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
import mysql.connector
import sys

class EditClientWindow(QDialog):
    def __init__(self, parent, db_connection, client_id):
        super().__init__(parent)
        self.db_connection = db_connection
        self.client_id = client_id
        self.init_ui()
        self.load_client_data()

    def init_ui(self):
        self.setWindowTitle('Editar Cliente')
        self.setGeometry(150, 150, 400, 300)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.lastname_input = QLineEdit()
        self.dni_input = QLineEdit()
        self.phone_input = QLineEdit()

        layout.addRow(QLabel('Nombre:'), self.name_input)
        layout.addRow(QLabel('Apellido:'), self.lastname_input)
        layout.addRow(QLabel('DNI:'), self.dni_input)
        layout.addRow(QLabel('Teléfono:'), self.phone_input)

        save_button = QPushButton('Guardar')
        save_button.clicked.connect(self.save_client)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def load_client_data(self):
        cursor = self.db_connection.cursor()
        query = "SELECT Nombre, Apellido, DNI, Telefono FROM Cliente WHERE ID_CLIENTE = %s"
        cursor.execute(query, (self.client_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            self.name_input.setText(result[0])
            self.lastname_input.setText(result[1])
            self.dni_input.setText(result[2])
            self.phone_input.setText(result[3])
        else:
            QMessageBox.warning(self, 'Error', 'Cliente no encontrado.')

    def save_client(self):
        name = self.name_input.text()
        lastname = self.lastname_input.text()
        dni = self.dni_input.text()
        phone = self.phone_input.text()

        if not (name and lastname and dni and phone):
            QMessageBox.warning(self, 'Advertencia', 'Todos los campos deben ser completados.')
            return

        cursor = self.db_connection.cursor()
        query = "UPDATE Cliente SET Nombre = %s, Apellido = %s, DNI = %s, Telefono = %s WHERE ID_CLIENTE = %s"
        cursor.execute(query, (name, lastname, dni, phone, self.client_id))
        self.db_connection.commit()
        cursor.close()

        QMessageBox.information(self, 'Éxito', 'Cliente actualizado exitosamente.')
        self.accept()  # Cierra el diálogo y regresa a la ventana principal
