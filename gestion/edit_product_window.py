from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox
import mysql.connector
import sys

class EditProductWindow(QDialog):
    def __init__(self, parent, db_connection, product_id):
        super().__init__(parent)
        self.db_connection = db_connection
        self.product_id = product_id
        self.init_ui()
        self.load_product_data()

    def init_ui(self):
        self.setWindowTitle('Editar Producto')
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

    def load_product_data(self):
        cursor = self.db_connection.cursor()
        query = "SELECT Nombre, Precio_Venta, Stock, Unidad, Tipo FROM Producto WHERE ID_PRODUCTO = %s"
        cursor.execute(query, (self.product_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            self.name_input.setText(result[0])
            self.price_input.setText(f"{result[1]:.2f}")
            self.stock_input.setText(str(result[2]))
            self.unit_input.setText(result[3])
            self.type_input.setText(result[4])
        else:
            QMessageBox.warning(self, 'Error', 'Producto no encontrado.')

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
            UPDATE Producto
            SET Nombre = %s, Precio_Venta = %s, Stock = %s, Unidad = %s, Tipo = %s
            WHERE ID_PRODUCTO = %s
            """
            cursor.execute(query, (name, price, stock, unit, type_, self.product_id))
            self.db_connection.commit()
            cursor.close()

            QMessageBox.information(self, 'Éxito', 'Producto actualizado exitosamente.')
            self.accept()  # Cierra el diálogo y regresa a la ventana principal
        except ValueError:
            QMessageBox.warning(self, 'Error', 'Precio Venta debe ser un número válido y Stock debe ser un número entero.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Error al actualizar el producto: {e}')
