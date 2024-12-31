from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QRadioButton, QVBoxLayout,
    QHBoxLayout, QPushButton, QMessageBox, QButtonGroup, QDialog, QTableWidget, QTableWidgetItem
)

class PaymentForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.payment_list = []  # Store payment details
    
    def init_ui(self):
        self.setWindowTitle("Form Pembayaran")
        self.resize(400, 300)

        # Layout Utama
        main_layout = QVBoxLayout()

        # Nama
        name_layout = QHBoxLayout()
        name_label = QLabel("Nama:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)

        # Jumlah Pembayaran
        amount_layout = QHBoxLayout()
        amount_label = QLabel("Jumlah Pembayaran (Rp):")
        self.amount_input = QLineEdit()
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)

        # Metode Pembayaran
        method_label = QLabel("Metode Pembayaran:")
        self.bank_radio = QRadioButton("Transfer Bank")
        self.card_radio = QRadioButton("Kartu Kredit")
        self.wallet_radio = QRadioButton("E-Wallet")
        self.cash_radio = QRadioButton("Cash")
        self.bank_radio.setChecked(True)

        # Grup Radio Button
        self.payment_group = QButtonGroup()
        self.payment_group.addButton(self.bank_radio)
        self.payment_group.addButton(self.card_radio)
        self.payment_group.addButton(self.wallet_radio)
        self.payment_group.addButton(self.cash_radio)

        # Layout Radio Button
        method_layout = QVBoxLayout()
        method_layout.addWidget(method_label)
        method_layout.addWidget(self.bank_radio)
        method_layout.addWidget(self.card_radio)
        method_layout.addWidget(self.wallet_radio)
        method_layout.addWidget(self.cash_radio)

        # Tombol Submit
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_payment)

        # Tombol Daftar Pembayaran
        self.list_button = QPushButton("Daftar Pembayaran")
        self.list_button.clicked.connect(self.show_payment_list)

        # Menambahkan ke Layout Utama
        main_layout.addLayout(name_layout)
        main_layout.addLayout(amount_layout)
        main_layout.addLayout(method_layout)
        main_layout.addWidget(self.submit_button)
        main_layout.addWidget(self.list_button)

        self.setLayout(main_layout)
    
    def submit_payment(self):
        name = self.name_input.text()
        amount = self.amount_input.text()
        method = self.payment_group.checkedButton().text()

        if not name or not amount:
            QMessageBox.warning(self, "Peringatan", "Semua bidang harus diisi!")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Kesalahan", "Jumlah pembayaran harus berupa angka positif!")
            return

        # Simpan pembayaran ke daftar
        self.payment_list.append((name, amount, method))

        QMessageBox.information(
            self, 
            "Berhasil", 
            f"Pembayaran berhasil!\n\nNama: {name}\nJumlah: Rp{amount:,.2f}\nMetode: {method}"
        )

    def show_payment_list(self):
        # Dialog untuk menampilkan daftar pembayaran
        payment_dialog = QDialog(self)
        payment_dialog.setWindowTitle("Daftar Pembayaran")
        payment_dialog.resize(600, 400)

        layout = QVBoxLayout()

        # Membuat QTableWidget
        table_widget = QTableWidget()
        table_widget.setRowCount(len(self.payment_list))
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(["Nama", "Jumlah", "Metode"])

        # Mengisi data ke dalam tabel
        for row, payment in enumerate(self.payment_list):
            table_widget.setItem(row, 0, QTableWidgetItem(payment[0]))  # Nama
            table_widget.setItem(row, 1, QTableWidgetItem(f"Rp{payment[1]:,.2f}"))  # Jumlah
            table_widget.setItem(row, 2, QTableWidgetItem(payment[2]))  # Metode

        # Menambahkan QTableWidget ke layout
        layout.addWidget(table_widget)
        payment_dialog.setLayout(layout)

        payment_dialog.exec_()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = PaymentForm()
    form.show()
    sys.exit(app.exec_())
