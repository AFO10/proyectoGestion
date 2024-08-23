from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
import mysql.connector
import sys

class AddProductWindow(QDialog):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.db_connection = db_connection
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Agregar Producto')
        self.setGeometry(150, 150, 400, 300)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.price_input = QLineEdit()
        self.stock_input = QLineEdit()
        self.unit_input = QLineEdit()
        self.type_input = QLineEdit()

        layout.addRow(QLabel('Nombre:'), self.name_input)
        layout.addRow(QLabel('Precio Venta:'), self.price_input)
        layout.addRow(QLabel('Stock:'), self.stock_input)
        layout.addRow(QLabel('Unidad:'), self.unit_input)
        layout.addRow(QLabel('Tipo:'), self.type_input)

        save_button = QPushButton('Guardar')
        save_button.clicked.connect(self.save_product)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_product(self):
        name = self.name_input.text()
        price_text = self.price_input.text()
        stock_text = self.stock_input.text()
        unit = self.unit_input.text()
        type_ = self.type_input.text()

        if not (name and price_text and stock_text and unit and type_):
            QMessageBox.warning(self, 'Advertencia', 'Todos los campos deben ser completados.')
            return

        try:
            price = float(price_text)
            stock = int(stock_text)

            cursor = self.db_connection.cursor()
            query = """
            INSERT INTO Producto (Nombre, Precio_Venta, Stock, Unidad, Tipo)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, price, stock, unit, type_))
            self.db_connection.commit()
            cursor.close()

            QMessageBox.information(self, 'Éxito', 'Producto agregado exitosamente.')
            self.accept()  # Cierra el diálogo y regresa a la ventana principal
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Precio Venta debe ser un número válido y Stock debe ser un número entero.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al agregar el producto: {e}')
