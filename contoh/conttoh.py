import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QMessageBox

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        layout = QVBoxLayout()
        
        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()
        
        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)
        
        self.button_login = QPushButton("Login")
        self.button_login.clicked.connect(self.login)
        
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)
        
        self.setLayout(layout)

    def login(self):
        username = self.input_username.text()
        password = self.input_password.text()

        if username == "" and password == "":
            
            QMessageBox.warning(self, "Login Failed", "Username or Password is incorrect")
        else:
            self.main_menu = MainMenu()
            self.main_menu.show()
            self.close()

class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu")
        layout = QVBoxLayout()

        self.label_menu = QLabel("Selamat Datang di Bioskop!")
        
        self.button_pesan = QPushButton("Pesan Tiket")
        self.button_pesan.clicked.connect(self.go_to_pesan)

        layout.addWidget(self.label_menu)
        layout.addWidget(self.button_pesan)
        
        self.setLayout(layout)

    def go_to_pesan(self):
        self.pesan_tiket = PesanTiket()
        self.pesan_tiket.show()
        self.close()

class PesanTiket(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pesan Tiket")
        layout = QVBoxLayout()

        self.label_film = QLabel("Pilih Film:")
        self.input_film = QLineEdit()

        self.label_jumlah = QLabel("Jumlah Tiket:")
        self.input_jumlah = QLineEdit()

        self.button_lanjut = QPushButton("Lanjutkan")
        self.button_lanjut.clicked.connect(self.go_to_bayar)

        layout.addWidget(self.label_film)
        layout.addWidget(self.input_film)
        layout.addWidget(self.label_jumlah)
        layout.addWidget(self.input_jumlah)
        layout.addWidget(self.button_lanjut)

        self.setLayout(layout)

    def go_to_bayar(self):
        self.bayar_tiket = BayarTiket(self.input_film.text(), self.input_jumlah.text())
        self.bayar_tiket.show()
        self.close()

class BayarTiket(QWidget):
    def __init__(self, film, jumlah):
        super().__init__()
        self.setWindowTitle("Bayar")
        layout = QVBoxLayout()

        self.label_konfirmasi = QLabel(f"Film: {film}\nJumlah: {jumlah}")

        self.button_bayar = QPushButton("Bayar")
        self.button_bayar.clicked.connect(self.go_to_struk)

        layout.addWidget(self.label_konfirmasi)
        layout.addWidget(self.button_bayar)

        self.setLayout(layout)

    def go_to_struk(self):
        self.struk_pembayaran = StrukPembayaran()
        self.struk_pembayaran.show()
        self.close()

class StrukPembayaran(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Struk Pembayaran")
        layout = QVBoxLayout()

        self.label_struk = QLabel("Pembayaran berhasil!\nTerima kasih sudah memesan.")

        layout.addWidget(self.label_struk)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec_())
