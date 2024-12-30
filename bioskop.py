import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableView, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtCore import QDate
from datetime import datetime
from PyQt5.QtCore import Qt



class login(QWidget):
        def __init__(self):
                super().__init__()
                self.login_ui()

        def login_ui(self):
                layout = QVBoxLayout()
                layout.setContentsMargins(20, 50, 20, 100)

        # QLineEdit untuk nama
                self.nama_login = QLineEdit(self)
                self.nama_login.setPlaceholderText("masukkan nama")
        # QLineEdit untuk alamat
                self.hp_login = QLineEdit(self)
                self.hp_login.setPlaceholderText("masukkan no hp")
        # QLineEdit untuk alamat
                self.email_login = QLineEdit(self)
                self.email_login.setPlaceholderText("masukkan email")
        # QlineEdit untuk password
                self.password = QLineEdit(self)
                self.password.setPlaceholderText(" masukkan Password")
                self.password.setEchoMode(QLineEdit.Password)
        # tombol login
                self.tombol_login = QPushButton("Login")
                self.tombol_login.clicked.connect(self.next_login)
        # tombol daftar
                self.tombol_daftar = QPushButton("daftar")
                self.tombol_daftar.clicked.connect(self.next_daftar)
                
        # susnan layout 
                label1 = QLabel("====== WELCOME ======")
                label1.setAlignment(Qt.AlignCenter)
                label1.setStyleSheet("""color: #2a3132;
                                        font-size: 16px; font-weight:
                                        bold; font-family: ubuntu ;
                                        ;""")
                label2 = QLabel("silahkan login terlebih dahulu sebelum melakukan pemesanan")
                label2.setAlignment(Qt.AlignCenter)
                layout.addWidget(label1)
                layout.addWidget(label2)
                layout.addWidget(QLabel("Nama :", self))
                layout.addWidget(self.nama_login)
                layout.addWidget(QLabel("no hp :", self))
                layout.addWidget(self.hp_login)
                layout.addWidget(QLabel("email :", self))
                layout.addWidget(self.email_login)
                layout.addWidget(QLabel("Password :", self))
                layout.addWidget(self.password)
                layout.addWidget(self.tombol_login)
                layout.addWidget(self.tombol_daftar)
                
                
                self.setLayout(layout)
                self.setWindowTitle("login")
                self.resize(400, 600) 
                
        def koneksi_database(self):
                return mysql.connector.connect(
                                host='localhost',
                                user = 'root',
                                password = '',
                                database = 'uas_bioskop'
                                
                        )
                
                self.setLayout(layout)
                self.setWindowTitle("login")
                self.setStyleSheet("background-color :#bdd2db;")
                self.setFixedSize(500, 800)
        
        def next_daftar(self):
                nama = self.nama_login.text().strip()
                no_hp = self.hp_login.text().strip()
                email = self.email_login.text().strip()
                password = self.password.text().strip()
                
                if not nama or not no_hp or not email or not password:
                        QMessageBox.warning(self, "Pendaftaran Gagal", "Silakan isi semua data.")
                        return

                if len(password) > 255:
                        QMessageBox.warning(self, "Pendaftaran Gagal", "Password terlalu panjang.")
                        return

                try:
                        connection = self.koneksi_database()
                        cursor = connection.cursor()
                        
                        query = "INSERT INTO customer (nama, email, no_hp, password) VALUES (%s, %s, %s, %s)"
                        cursor.execute(query, (nama, email, no_hp, password))
                        connection.commit()
                        
                        QMessageBox.information(self, "Berhasil", "Akun berhasil dibuat.")
                except mysql.connector.Error as e:
                        QMessageBox.critical(self, "Error", f"Gagal membuat akun: {e}")
                finally:
                        if 'connection' in locals() and connection.is_connected():
                                cursor.close()
                                connection.close()


        def next_login(self):
                email = self.email_login.text().strip()
                password = self.password.text().strip()

                if not email or not password:
                        QMessageBox.warning(self, "Login Gagal", "cukup isi email dan password.")
                        return

                try:
                        connection = self.koneksi_database()
                        cursor = connection.cursor()
                        query = "SELECT * FROM customer WHERE email = %s AND password = %s"
                        cursor.execute(query, (email, password))
                        result = cursor.fetchone()

                        if result:
                                QMessageBox.information(self, "Berhasil", "Login berhasil!")
                        # Tambahkan logika untuk berpindah ke halaman berikutnya di sini
                        else:
                                QMessageBox.warning(self, "Login Gagal", "Email atau password salah.")
                except mysql.connector.Error as e:
                        QMessageBox.critical(self, "Error", f"Gagal login: {e}")
                finally:
                        if 'connection' in locals() and connection.is_connected():
                                cursor.close()
                                connection.close()
                                
        def masuk_pesan_tiket(self):
                self.pesam_tiket.shoe()
                self.close()
class daftar_film(QWidget):
        def __init__(self):
                super().__init__()
                self.film_ui()
                
class pesan_tiket(QWidget):
        def __init__(self):
                super().__init__()
                self.tiket_ui()
                
class pembayaran(QWidget):
        def __init__(self):
                self.pembayaran_ui()
                
class tket_qr(QWidget):
        def __init__(self):
                self.qr_ui()
                

# Main program
if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = login()
        window.show()
        sys.exit(app.exec_())