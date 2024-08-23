import sys
from agregarProducto import AgregarProducto
import mysql.connector
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QSizePolicy, QHeaderView
from add_client_window import AddClientWindow
from edit_client_window import EditClientWindow
from add_product_window import AddProductWindow
from edit_product_window import EditProductWindow

venta = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.table_windows = []
        self.db_connection = self.connect_to_db()
        self.current_table = None

    def connect_to_db(self):
        try:
            cnx = mysql.connector.connect(
                host="localhost",
                user="root",
                password="FEsor1135.",
                database="elrocco"
            )
            return cnx
        except mysql.connector.Error as err:
            QMessageBox.critical(self, 'Error de conexión', f'No se pudo conectar a la base de datos: {err}')
            sys.exit()

    def init_ui(self):
        self.setWindowTitle('Menú Principal')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        buttons = [
            ('Cliente', self.show_cliente),
            ('Proveedor', self.show_proveedor),
            ('Empleado', self.show_empleado),
            ('Producto', self.show_producto),
            ('Orden Pedido', self.show_orden_pedido),
            ('Realizar Venta', self.show_orden_venta),
            ('Cerrar Sesión', self.close)
        ]

        for text, func in buttons:
            button = QPushButton(text)
            button.clicked.connect(func)
            layout.addWidget(button)
            if text == 'Cerrar Sesión':
                button.setObjectName('logout_button')
            else:
                button.setObjectName('menu_button')

        central_widget.setLayout(layout)
        

    def show_table(self, columns, data,venta):
        table_window = QWidget()
        table_window.setWindowTitle('Tabla de Datos')
        table_window.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        table = QTableWidget()
        table.setRowCount(len(data))
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)

        header = table.horizontalHeader()
        for col in range(len(columns)):
            header.setSectionResizeMode(col, QHeaderView.Stretch)

        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for row_idx, row_data in enumerate(data):
            for col_idx, item in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

        layout.addWidget(table)

        button_layout = QHBoxLayout()

        if venta:
            agregarProducto = QPushButton('Agregar producto')
            finalizarVenta = QPushButton('Finalizar Venta')

            agregarProducto.setObjectName('agregarProducto')
            finalizarVenta.setObjectName('finalizarVenta')

            agregarProducto.clicked.connect(self.agregar_item)
            finalizarVenta.clicked.connect(self.finalizar_venta)

            button_layout.addWidget(agregarProducto)
            button_layout.addWidget(finalizarVenta)
        else:
            add_button = QPushButton('Agregar')
            edit_button = QPushButton('Editar')
            delete_button = QPushButton('Eliminar')

            add_button.setObjectName('add_button')
            edit_button.setObjectName('edit_button')
            delete_button.setObjectName('delete_button')

            add_button.clicked.connect(self.add_item)
            edit_button.clicked.connect(self.edit_item)
            delete_button.clicked.connect(self.delete_item)

            button_layout.addWidget(add_button)
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)

        close_button = QPushButton('Cerrar')
        close_button.setObjectName('close_button')
        close_button.clicked.connect(table_window.close)
        layout.addWidget(close_button)

        table_window.setLayout(layout)
        table_window.show()

        self.table_windows.append(table_window)

    def add_item(self):
        if self.current_table == 'Cliente':
            self.add_client_window = AddClientWindow(self, self.db_connection)
            self.add_client_window.exec_()  # Usa exec_() en lugar de show()
        else:
            if self.current_table == 'Producto':
                self.add_product_window = AddProductWindow(self, self.db_connection)
                self.add_product_window.exec_()  # Usa exec_() en lugar de show()
            else:
                QMessageBox.information(self, 'Agregar', 'Agregar ítem no implementado aún para esta tabla.')

    def agregar_item(self):
        self.agregarProducto = AgregarProducto(self, self.db_connection)
        self.agregarProducto.exec_()

    def finalizar_venta(self):
        print()

    def edit_item(self):
        if self.current_table == 'Cliente':
            selected_item = self.get_selected_item()
            if selected_item:
                client_id = selected_item[0]  # Asumiendo que el ID es la primera columna
                self.edit_client_window = EditClientWindow(self, self.db_connection, client_id)
                self.edit_client_window.exec_()  # Usa exec_() para mostrar el diálogo de manera modal
            else:
                QMessageBox.warning(self, 'Editar', 'Por favor, seleccione un cliente para editar.')
        else:
            if self.current_table == 'Producto':
                selected_item = self.get_selected_item()
                if selected_item:
                    product_id = selected_item[0]  # Asumiendo que el ID es la primera columna
                    self.edit_product_window = EditProductWindow(self, self.db_connection, product_id)
                    self.edit_product_window.exec_()  # Usa exec_() para mostrar el diálogo de manera modal
                else:
                    QMessageBox.warning(self, 'Editar', 'Por favor, seleccione un cliente para editar.')

    def get_selected_item(self):
        table_window = self.get_current_table_window()
        if table_window:
            table = table_window.findChild(QTableWidget)
            selected_items = table.selectedItems()
            if selected_items:
                selected_row = selected_items[0].row()
                row_data = [table.item(selected_row, col).text() for col in range(table.columnCount())]
                return row_data
        return None

    def get_current_table_window(self):
        # Retorna la ventana de tabla actualmente visible, si existe
        if self.table_windows:
            return self.table_windows[-1]
        return None


    def delete_item(self):
        if self.current_table == 'Cliente':
            selected_item = self.get_selected_item()
            if selected_item:
                client_id = selected_item[0]  # Asumiendo que el ID es la primera columna
                reply = QMessageBox.question(
                    self, 'Confirmar Eliminación',
                    f'¿Estás seguro de que quieres eliminar el cliente con ID {client_id}?',
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    cursor = self.db_connection.cursor()
                    query = "DELETE FROM Cliente WHERE ID_CLIENTE = %s"
                    cursor.execute(query, (client_id,))
                    self.db_connection.commit()
                    cursor.close()

                    QMessageBox.information(self, 'Éxito', 'Cliente eliminado exitosamente.')
                    self.show_cliente()  # Recargar la tabla para reflejar los cambios
                else:
                    QMessageBox.information(self, 'Cancelado', 'Eliminación cancelada.')
            else:
                QMessageBox.warning(self, 'Eliminar', 'Por favor, seleccione un cliente para eliminar.')
        else:
            QMessageBox.information(self, 'Eliminar', 'Eliminar ítem no implementado aún para esta tabla.')


    def fetch_data(self, query):
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data

    def show_cliente(self):
        venta = False
        self.current_table = 'Cliente'
        columns = ["ID_CLIENTE", "Nombre", "Apellido", "DNI", "Telefono"]
        query = "SELECT ID_CLIENTE, Nombre, Apellido, DNI, Telefono FROM Cliente"
        data = self.fetch_data(query)
        self.show_table(columns, data, venta)

    def show_proveedor(self):
        venta = False
        self.current_table = 'Proveedor'
        columns = ["ID_PROVEEDOR", "Nombre", "RUC"]
        query = "SELECT ID_PROVEEDOR, Nombre, RUC FROM Proveedor"
        data = self.fetch_data(query)
        self.show_table(columns, data, venta)

    def show_empleado(self):
        venta = False
        self.current_table = 'Empleado'
        columns = ["ID_EMPLEADO", "Nombre", "Apellido", "DNI"]
        query = "SELECT ID_EMPLEADO, Nombre, Apellido, DNI FROM Empleado"
        data = self.fetch_data(query)
        self.show_table(columns, data, venta)

    def show_producto(self):
        venta = False
        self.current_table = 'Producto'
        columns = ["ID_PRODUCTO", "Nombre", "Precio_Venta", "Stock", "Unidad", "Tipo"]
        query = "SELECT ID_PRODUCTO, Nombre, Precio_Venta, Stock, Unidad, Tipo FROM Producto"
        data = self.fetch_data(query)
        self.show_table(columns, data, venta)

    def show_orden_pedido(self):
        venta = False
        self.current_table = 'Pedido'
        columns = ["ID_PEDIDO", "Fecha", "ID_EMPLEADO", "ID_PROVEEDOR"]
        query = "SELECT ID_PEDIDO, Fecha, ID_EMPLEADO, ID_PROVEEDOR FROM Pedido"
        data = self.fetch_data(query)
        self.show_table(columns, data, venta)



    def show_orden_venta(self):
        ventas = []
        venta = True
        self.current_table = 'Compra'
        columns = ["ID_PRODUCTO", "CANTIDAD"]
        self.show_table(columns, ventas, venta)
