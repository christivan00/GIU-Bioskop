import sys
import pymysql
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QRadioButton, QHBoxLayout, QGridLayout, QFrame, QDialog, QGroupBox, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import qrcode
import random


# Fungsi untuk menghubungkan ke database dan mengambil data film
def get_film_data():
    conn = pymysql.connect(host='localhost', user='root', password='', database='uas_bioskop')
    cursor = conn.cursor()
    query = "SELECT id_film, nama_film, harga, durasi, genre FROM film"
    cursor.execute(query)
    films = cursor.fetchall()
    cursor.close()
    conn.close()
    return films


class login(QWidget):
    def __init__(self):
        super().__init__()
        self.login_ui()

    def login_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 50, 20, 100)

        self.nama_login = QLineEdit(self)
        self.nama_login.setPlaceholderText("masukkan nama")
        self.hp_login = QLineEdit(self)
        self.hp_login.setPlaceholderText("masukkan no hp")
        self.email_login = QLineEdit(self)
        self.email_login.setPlaceholderText("masukkan email")
        self.password = QLineEdit(self)
        self.password.setPlaceholderText(" masukkan Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.tombol_login = QPushButton("Login")
        self.tombol_login.clicked.connect(self.next_login)
        self.tombol_daftar = QPushButton("daftar")
        self.tombol_daftar.clicked.connect(self.next_daftar)

        label1 = QLabel("====== WELCOME ======")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("""color: #2a3132;
                                font-size: 16px; font-weight:
                                bold; font-family: ubuntu ;""")
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
        return pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='uas_bioskop'
        )

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

            QMessageBox.information(self, "Berhasil", "Akun berhasil dibuat. silahkan login")
        except pymysql.MySQLError as e:
            QMessageBox.critical(self, "Error", f"Gagal membuat akun: {e}")
        finally:
            if 'connection' in locals() and connection.open:
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
                self.open_film_gallery()
            else:
                QMessageBox.warning(self, "Login Gagal", "Email atau password salah.")
        except pymysql.MySQLError as e:
            QMessageBox.critical(self, "Error", f"Gagal login: {e}")
        finally:
            if 'connection' in locals() and connection.open:
                cursor.close()
                connection.close()

    def open_film_gallery(self):
        self.film_gallery = FilmGallery()
        self.film_gallery.show()
        self.close()


class FilmGallery(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_film = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Daftar Film")
        self.resize(400, 600)

        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        label1 = QLabel('DAFTAR FILM')
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("font-size: 18px; font-weight: bold;")

        films = get_film_data()

        for index, film in enumerate(films):
            frame = QFrame()
            frame_layout = QVBoxLayout()

            pixmap = QPixmap(f"gambar/{film[1]}.jpg")
            pixmap = pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon = QIcon(pixmap)
            button = QPushButton()
            button.setIcon(icon)
            button.setIconSize(pixmap.size())
            button.clicked.connect(lambda _, f=film: self.select_film(f))

            judul_label = QLabel(film[1])
            judul_label.setAlignment(Qt.AlignCenter)
            judul_label.setStyleSheet("font-weight: bold; font-size: 14px;")

            frame_layout.addWidget(button)
            frame_layout.addWidget(judul_label)
            frame.setLayout(frame_layout)
            frame.setFrameShape(QFrame.StyledPanel)

            row = index // 2
            col = index % 2
            grid_layout.addWidget(frame, row, col)

        main_layout.addWidget(label1)
        main_layout.addLayout(grid_layout)

        footer_layout = QHBoxLayout()
        confirm_button = QPushButton("Konfirmasi Pilihan")
        confirm_button.setStyleSheet("font-size: 14px;")
        confirm_button.clicked.connect(self.confirm_selection)
        footer_layout.addWidget(confirm_button, alignment=Qt.AlignCenter)

        main_layout.addLayout(footer_layout)
        self.setLayout(main_layout)

    def select_film(self, film):
        self.selected_film = film

    def confirm_selection(self):
        if self.selected_film:
            self.open_pemesanan_tiket(self.selected_film)
        else:
            no_selection_dialog = QDialog(self)
            no_selection_dialog.setWindowTitle("Peringatan")
            no_selection_dialog.resize(300, 150)
            layout = QVBoxLayout()
            label = QLabel("Anda belum memilih film!")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            no_selection_dialog.setLayout(layout)
            no_selection_dialog.exec_()

    def open_pemesanan_tiket(self, film):
        self.pemesanan_tiket = PemesananTiket(film)
        self.pemesanan_tiket.show()
        self.close()


class PemesananTiket(QWidget):
    def __init__(self, film):
        super().__init__()
        self.film = film
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Pemesanan Tiket")
        self.resize(500, 700)

        layout = QVBoxLayout()

        pixmap = QPixmap(f"gambar/{self.film[1]}.jpg")
        if pixmap.isNull():
            pixmap = QPixmap("gambar/default.jpg")
        pixmap = pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon = QIcon(pixmap)
        gambar_label = QLabel()
        gambar_label.setPixmap(icon.pixmap(150, 200))

        label1 = QLabel(f"Film: {self.film[1]}")
        label1.setStyleSheet("font-size: 16px; font-weight: bold;")
        label2 = QLabel(f"Durasi: {self.film[3]} min")
        label3 = QLabel(f"Genre: {self.film[4]}")

        hari_group = QGroupBox("Pilih Hari")
        hari_layout = QVBoxLayout()
        hari_hari_ini = QRadioButton("Hari ini")
        hari_besok = QRadioButton("Besok")
        hari_lusa = QRadioButton("Lusa")
        hari_layout.addWidget(hari_hari_ini)
        hari_layout.addWidget(hari_besok)
        hari_layout.addWidget(hari_lusa)
        hari_group.setLayout(hari_layout)

        jam_group = QGroupBox("Pilih Jam")
        jam_layout = QVBoxLayout()
        jam_0900 = QRadioButton("09:00")
        jam_1200 = QRadioButton("12:00")
        jam_1600 = QRadioButton("16:00")
        jam_layout.addWidget(jam_0900)
        jam_layout.addWidget(jam_1200)
        jam_layout.addWidget(jam_1600)
        jam_group.setLayout(jam_layout)

        label_jumlah_tiket = QLabel("Jumlah Tiket:")
        self.jumlah_tiket = QLineEdit(self)
        self.jumlah_tiket.setPlaceholderText("Masukkan jumlah tiket")

        label_kursi = QLabel("Pilih Kursi:")
        self.table_kursi = QTableWidget(5, 5)
        self.table_kursi.setHorizontalHeaderLabels([f"Kursi {i+1}" for i in range(5)])
        self.table_kursi.setVerticalHeaderLabels([f"Row {i+1}" for i in range(5)])

        for row in range(5):
            for col in range(5):
                item = QTableWidgetItem()
                item.setText("Tersedia")
                self.table_kursi.setItem(row, col, item)

        tombol_pesan = QPushButton("Pesan Tiket")
        tombol_pesan.clicked.connect(self.pesan_tiket)

        layout.addWidget(gambar_label)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(hari_group)
        layout.addWidget(jam_group)
        layout.addWidget(label_jumlah_tiket)
        layout.addWidget(self.jumlah_tiket)
        layout.addWidget(label_kursi)
        layout.addWidget(self.table_kursi)
        layout.addWidget(tombol_pesan)

        self.setLayout(layout)

    def pesan_tiket(self):
        jumlah = self.jumlah_tiket.text()
        if not jumlah.isdigit():
            QMessageBox.warning(self, "Error", "Jumlah tiket harus berupa angka.")
            return
        self.open_pembayaran()

    def open_pembayaran(self):
        self.pembayaran = Pembayaran(self.film, self.jumlah_tiket.text())
        self.pembayaran.show()
        self.close()


class Pembayaran(QWidget):
    def __init__(self, film, jumlah_tiket):
        super().__init__()
        self.film = film
        self.jumlah_tiket = jumlah_tiket
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Pembayaran Tiket")
        self.resize(500, 700)

        layout = QVBoxLayout()

        label1 = QLabel(f"Nama Film: {self.film[1]}")
        label2 = QLabel(f"Jumlah Tiket: {self.jumlah_tiket}")
        harga_tiket = int(self.film[2])
        total_harga = harga_tiket * int(self.jumlah_tiket)
        biaya_layanan = 5000 * int(self.jumlah_tiket)
        total_bayar = total_harga + biaya_layanan

        label3 = QLabel(f"Harga Tiket: {harga_tiket} x {self.jumlah_tiket} = {total_harga}")
        label4 = QLabel(f"Biaya Layanan: {biaya_layanan}")
        label5 = QLabel(f"Total Bayar: {total_bayar}")

        metode_group = QGroupBox("Metode Pembayaran")
        metode_layout = QVBoxLayout()
        qris = QRadioButton("QRIS")
        dana = QRadioButton("Dana")
        gopay = QRadioButton("Gopay")
        cash = QRadioButton("Cash")
        kartu_kredit = QRadioButton("Kartu Kredit")
        metode_layout.addWidget(qris)
        metode_layout.addWidget(dana)
        metode_layout.addWidget(gopay)
        metode_layout.addWidget(cash)
        metode_layout.addWidget(kartu_kredit)
        metode_group.setLayout(metode_layout)

        tombol_bayar = QPushButton("Selesaikan Pembayaran Anda")
        tombol_bayar.clicked.connect(self.selesaikan_pembayaran)

        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)
        layout.addWidget(label4)
        layout.addWidget(label5)
        layout.addWidget(metode_group)
        layout.addWidget(tombol_bayar)

        self.setLayout(layout)

    def selesaikan_pembayaran(self):
        ticket_id = random.randint(1000, 9999)  # ID tiket acak
        qr_data = f"Film: {self.film[1]}\nJumlah Tiket: {self.jumlah_tiket}\nID Tiket: {ticket_id}"
        self.generate_eticket(qr_data)

    def generate_eticket(self, qr_data):
        qr = qrcode.make(qr_data)
        qr.save("eticket.png")
        qr.show()
        QMessageBox.information(self, "Pembayaran Sukses", "Pembayaran berhasil! E-tiket telah dibuat.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = login()
    login_window.show()
    sys.exit(app.exec_())
    