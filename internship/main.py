import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QDateEdit,
    QSpinBox, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView
)
from PySide6.QtCore import Qt
import mysql.connector
from mysql.connector import Error

class BillingForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Billing Form")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.customer_name_edit = QLineEdit()
        self.form_layout.addRow(QLabel("Customer Name:"), self.customer_name_edit)

        self.customer_email_edit = QLineEdit()
        self.form_layout.addRow(QLabel("Customer Email:"), self.customer_email_edit)

        self.customer_phone_edit = QLineEdit()
        self.form_layout.addRow(QLabel("Customer Phone:"), self.customer_phone_edit)

        self.customer_address_edit = QLineEdit()
        self.form_layout.addRow(QLabel("Customer Address:"), self.customer_address_edit)

        self.bill_date_edit = QDateEdit()
        self.bill_date_edit.setCalendarPopup(True)
        self.form_layout.addRow(QLabel("Bill Date:"), self.bill_date_edit)

        self.total_edit = QSpinBox()
        self.total_edit.setRange(0, 1000000)
        self.form_layout.addRow(QLabel("Total:"), self.total_edit)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(0)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Bill ID" ,"Bill Date", "Total","Customer Name"])
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(self.table_widget)

        self.retrieve_button = QPushButton("Retrieve Bills")
        self.retrieve_button.clicked.connect(self.retrieve_bills)
        self.layout.addWidget(self.retrieve_button)

        self.retrieve_customers_button = QPushButton("Retrieve Customers")
        self.retrieve_customers_button.clicked.connect(self.retrieve_customers)
        self.layout.addWidget(self.retrieve_customers_button)

        self.customer_table_widget = QTableWidget()
        self.customer_table_widget.setRowCount(0)
        self.customer_table_widget.setColumnCount(4)
        self.customer_table_widget.setHorizontalHeaderLabels([ "Name", "Email", "Phone", "Address"])
        self.customer_table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(self.customer_table_widget)

    def save_data(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="billing_systems"
            )

            cursor = db.cursor()

            query = "INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)"
            values = (
                self.customer_name_edit.text(),
                self.customer_email_edit.text(),
                self.customer_phone_edit.text(),
                self.customer_address_edit.text()
            )
            cursor.execute(query, values)
            customer_id = cursor.lastrowid

            query = "INSERT INTO bills (customer_id, bill_date, total) VALUES (%s, %s, %s)"
            values = (
                customer_id,
                self.bill_date_edit.date().toString("yyyy-MM-dd"),
                self.total_edit.value()
            )
            cursor.execute(query, values)

            db.commit()
            cursor.close()
            db.close()

        except Error as e:
            print("Error while saving data:", e)

    def retrieve_bills(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="billing_systems"
            )

            cursor = db.cursor()

            query = """
                SELECT bills.id,bills.bill_date,bills.total,customers.name
                FROM bills
                JOIN customers ON bills.customer_id = customers.id
            """
            cursor.execute(query)
            results = cursor.fetchall()

            self.table_widget.setRowCount(0)  # Clear previous data

            for row_number, row_data in enumerate(results):
                self.table_widget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            cursor.close()
            db.close()

        except Error as e:
            print("Error while retrieving bills:", e)

    def retrieve_customers(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="billing_systems"
            )

            cursor = db.cursor()

            query = "SELECT  name, email, phone, address FROM customers"
            cursor.execute(query)
            results = cursor.fetchall()

            self.customer_table_widget.setRowCount(0)

            for row_number, row_data in enumerate(results):
                self.customer_table_widget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.customer_table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            cursor.close()
            db.close()

        except Error as e:
            print("Error while retrieving customers:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BillingForm()
    window.show()
    sys.exit(app.exec())
