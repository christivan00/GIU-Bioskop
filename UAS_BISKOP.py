import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout,QComboBox,QButtonGroup,QRadioButton,QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class login(QWidget):
    def __init__(self):
        super().__init__()
        self.login_ui()

    def login_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 50, 20, 200)

        # QLineEdit untuk nama
        self.nama_login = QLineEdit(self)
        self.nama_login.setPlaceholderText("masukkan nama")
        
        # QLineEdit untuk no hp
        self.hp_login = QLineEdit(self)
        self.hp_login.setPlaceholderText("masukkan no hp")
        
        # QLineEdit untuk email
        self.email_login = QLineEdit(self)
        self.email_login.setPlaceholderText("masukkan email")
        
        # QLineEdit untuk password
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("masukkan Password")
        self.password.setEchoMode(QLineEdit.Password)

        # Tombol login
        self.tombol_login = QPushButton("Login")
        self.tombol_login.clicked.connect(self.next_login)
        
        # Tombol daftar
        self.tombol_daftar = QPushButton("Daftar")
        self.tombol_daftar.clicked.connect(self.next_daftar)
        
        # Susunan layout
        label1 = QLabel("====== WELCOME ======")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("""color: #2a3132; font-size: 16px; font-weight: bold; font-family: ubuntu;""")
        
        label2 = QLabel("Silakan login terlebih dahulu sebelum melakukan pemesanan")
        label2.setAlignment(Qt.AlignCenter)

        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(QLabel("Nama:", self))
        layout.addWidget(self.nama_login)
        layout.addWidget(QLabel("No HP:", self))
        layout.addWidget(self.hp_login)
        layout.addWidget(QLabel("Email:", self))
        layout.addWidget(self.email_login)
        layout.addWidget(QLabel("Password:", self))
        layout.addWidget(self.password)
        layout.addWidget(self.tombol_login)
        layout.addWidget(self.tombol_daftar)
        
        self.setLayout(layout)
        self.setWindowTitle("Login")
        self.resize(400, 600)

    def koneksi_database(self):
        return mysql.connector.connect(
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
            QMessageBox.warning(self, "Login Gagal", "Silakan isi email dan password.")
            return

        try:
            connection = self.koneksi_database()
            cursor = connection.cursor()
            query = "SELECT * FROM customer WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            result = cursor.fetchone()

            if result:
                # Mendapatkan nama pengguna setelah login berhasil
                nama_user = result[1]  # Indeks 1 sesuai dengan posisi nama pada tabel customer
                QMessageBox.information(self, "Berhasil", "Login berhasil!")
                # Pindah ke halaman daftar film dan kirimkan nama pengguna
                self.daftar_film = daftar_film(nama_user)
                self.daftar_film.show()
                self.close()
            else:
                QMessageBox.warning(self, "Login Gagal", "Email atau password salah.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Gagal login: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()


class daftar_film(QWidget):
    def __init__(self, nama_user):
        super().__init__()
        self.nama_user = nama_user  # Menyimpan nama pengguna
        self.film_ui()

    def koneksi_database(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='uas_bioskop'
        )

    def film_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 10, 20, 200)

        # Label akun di bagian atas
        label_akun = QLabel(f"Akun: {self.nama_user}")
        label_akun.setAlignment(Qt.AlignLeft)
        label_akun.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        layout.addWidget(label_akun)

        # Label judul
        label1 = QLabel("Daftar Film")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label1)

        # Grid Layout untuk menampilkan film dalam kotak
        self.gridLayout = QGridLayout()
        layout.addLayout(self.gridLayout)

        # Ambil data film dari database
        self.get_film_data()

        self.setLayout(layout)
        self.setWindowTitle("Daftar Film")
        self.resize(400, 600)

    def get_film_data(self):
        try:
            connection = self.koneksi_database()
            cursor = connection.cursor()
            query = "SELECT id_film, nama_film, harga, durasi, genre, gambar_film FROM film"
            cursor.execute(query)
            films = cursor.fetchall()

            row, col = 0, 0
            for film in films:
                id_film, nama_film, harga, durasi, genre, gambar_path = film
                
                # Pastikan gambar_path benar-benar valid
                gambar_path = gambar_path.replace('/', '\\')  # Mengganti semua '/' dengan '\\' untuk path Windows

                # Membuat QPixmap untuk menampilkan gambar
                pixmap = QPixmap(gambar_path)
                pixmap = pixmap.scaled(100, 150, Qt.KeepAspectRatio)
                
                # Membuat label untuk gambar film
                image_label = QLabel(self)
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignCenter)
                image_label.setStyleSheet("border: 1px solid black; padding: 5px; margin: 10px;")
                image_label.mousePressEvent = lambda event, id_film=id_film: self.open_pemesanan(id_film)  # Fungsi click

                name_label = QLabel(nama_film)
                name_label.setAlignment(Qt.AlignCenter)

                price_label = QLabel(f"Harga: {harga}")
                price_label.setAlignment(Qt.AlignCenter)

                # Menambahkan label gambar ke grid
                self.gridLayout.addWidget(name_label, row, col)
                self.gridLayout.addWidget(image_label, row + 1, col)
                self.gridLayout.addWidget(price_label, row + 2, col)

                # Menambah kolom, jika lebih dari 1 film, pindah ke baris berikutnya
                col += 1
                if col > 1:  # Menampilkan 2 film per baris
                    col = 0
                    row += 3

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Gagal mengambil data film: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def open_pemesanan(self, id_film):
        # Pindah ke halaman pemesanan setelah klik gambar
        self.pemesanan = pemesanan(id_film)
        self.pemesanan.show()
        self.close()


class pemesanan(QWidget):
    def __init__(self, id_film):
        super().__init__()
        self.id_film = id_film  # Menyimpan ID film yang dipilih
        self.pemesanan_ui()

    def koneksi_database(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='uas_bioskop'
        )

    def pemesanan_ui(self):
        # Buat layout terlebih dahulu
        self.layout_pemesanan = QVBoxLayout()

        # Ambil data film berdasarkan id
        self.get_film_detail()

        # Set layout setelah mendapatkan detail film
        self.setLayout(self.layout_pemesanan)
        self.setWindowTitle("Pemesanan Film")
        self.resize(400, 600)

    def get_film_detail(self):
        try:
            connection = self.koneksi_database()
            cursor = connection.cursor()
            query = f"SELECT nama_film, harga, durasi, genre FROM film WHERE id_film = {self.id_film}"
            cursor.execute(query)
            film = cursor.fetchone()

            if film:
                nama_film, harga, durasi, genre = film

                # Menampilkan detail film
                self.layout_pemesanan.addWidget(QLabel(f"Nama Film: {nama_film}"))
                self.layout_pemesanan.addWidget(QLabel(f"Durasi: {durasi}"))
                self.layout_pemesanan.addWidget(QLabel(f"Genre: {genre}"))
                self.layout_pemesanan.addWidget(QLabel(f"Harga: {harga}"))

                # Menambahkan radio button untuk pilihan hari tayang
                self.layout_pemesanan.addWidget(QLabel("Pilih Hari Tayang:"))
                self.hari_group = QButtonGroup()
                hari_options = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
                hari_layout = QVBoxLayout()  # Layout untuk radio button hari tayang
                for i, day in enumerate(hari_options):
                    radio_button = QRadioButton(day)
                    self.hari_group.addButton(radio_button)
                    hari_layout.addWidget(radio_button)  # Menambahkan radio button ke layout vertikal
                self.layout_pemesanan.addLayout(hari_layout)  # Menambahkan layout hari tayang ke layout utama

                # Menambahkan radio button untuk jam tayang
                self.layout_pemesanan.addWidget(QLabel("Pilih Jam Tayang:"))
                self.jam_group = QButtonGroup()
                jam_options = ["10:00", "13:00", "16:00", "19:00"]
                jam_layout = QVBoxLayout()  # Layout untuk radio button jam tayang
                for i, jam in enumerate(jam_options):
                    radio_button = QRadioButton(jam)
                    self.jam_group.addButton(radio_button)
                    jam_layout.addWidget(radio_button)  # Menambahkan radio button ke layout vertikal
                self.layout_pemesanan.addLayout(jam_layout)  # Menambahkan layout jam tayang ke layout utama

                # Input nomor kursi
                self.layout_pemesanan.addWidget(QLabel("Masukkan Nomor Kursi:"))
                self.kursi_input = QLineEdit(self)
                self.layout_pemesanan.addWidget(self.kursi_input)

                # Pilihan metode pembayaran
                self.layout_pemesanan.addWidget(QLabel("Pilih Metode Pembayaran:"))
                self.metode_combo = QComboBox(self)
                self.metode_combo.addItems(["Cash", "Debit", "Credit", "E-wallet"])
                self.layout_pemesanan.addWidget(self.metode_combo)

                # Tombol Pemesanan
                self.pesan_button = QPushButton("Pesan", self)
                self.pesan_button.clicked.connect(self.pesan_film)
                self.layout_pemesanan.addWidget(self.pesan_button)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Gagal mengambil detail film: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def pesan_film(self):
        # Validasi input dan proses pemesanan
        hari_tayang = self.hari_group.checkedButton().text() if self.hari_group.checkedButton() else None
        jam_tayang = self.jam_group.checkedButton().text() if self.jam_group.checkedButton() else None
        kursi = self.kursi_input.text().strip()
        metode_pembayaran = self.metode_combo.currentText()

        if not all([hari_tayang, jam_tayang, kursi, metode_pembayaran]):
            QMessageBox.warning(self, "Pemesanan Gagal", "Pastikan semua data terisi dengan benar.")
            return

        # Proses pemesanan (misalnya menyimpan ke database, dll)
        QMessageBox.information(self, "Pemesanan Berhasil", "Pemesanan Anda berhasil!")
        
class pemesanan(QWidget):
    def __init__(self, id_film):
        super().__init__()
        self.id_film = id_film  # Menyimpan ID film yang dipilih
        self.pemesanan_ui()

    def koneksi_database(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='uas_bioskop'
        )

    def pemesanan_ui(self):
        # Buat layout terlebih dahulu
        self.layout_pemesanan = QVBoxLayout()
        self.layout_pemesanan.setContentsMargins(20, 10, 20, 200)


        # Ambil data film berdasarkan id
        self.get_film_detail()

        # Set layout setelah mendapatkan detail film
        self.setLayout(self.layout_pemesanan)
        self.setWindowTitle("Pemesanan Film")
        self.resize(400, 600)

    def get_film_detail(self):
        try:
            connection = self.koneksi_database()
            cursor = connection.cursor()
            query = f"SELECT nama_film, harga, durasi, genre FROM film WHERE id_film = {self.id_film}"
            cursor.execute(query)
            film = cursor.fetchone()

            if film:
                nama_film, harga, durasi, genre = film

                # Menampilkan detail film
                self.layout_pemesanan.addWidget(QLabel(f"Nama Film: {nama_film}"))
                self.layout_pemesanan.addWidget(QLabel(f"Durasi: {durasi}"))
                self.layout_pemesanan.addWidget(QLabel(f"Genre: {genre}"))
                self.layout_pemesanan.addWidget(QLabel(f"Harga: {harga}"))

                # Menambahkan radio button untuk pilihan hari tayang
                self.layout_pemesanan.addWidget(QLabel("Pilih Hari Tayang:"))
                self.hari_group = QButtonGroup()
                hari_options = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
                
                # Horizontal Layout untuk radio button hari
                hari_layout = QHBoxLayout()
                for day in hari_options:
                    radio_button = QRadioButton(day)
                    self.hari_group.addButton(radio_button)
                    hari_layout.addWidget(radio_button)
                self.layout_pemesanan.addLayout(hari_layout)

                # Menambahkan radio button untuk jam tayang
                self.layout_pemesanan.addWidget(QLabel("Pilih Jam Tayang:"))
                self.jam_group = QButtonGroup()
                jam_options = ["10:00", "13:00", "16:00", "19:00"]
                
                # Horizontal Layout untuk radio button jam
                jam_layout = QHBoxLayout()
                for jam in jam_options:
                    radio_button = QRadioButton(jam)
                    self.jam_group.addButton(radio_button)
                    jam_layout.addWidget(radio_button)
                self.layout_pemesanan.addLayout(jam_layout)

                # Input nomor kursi
                self.layout_pemesanan.addWidget(QLabel("Masukkan Nomor Kursi:"))
                self.kursi_input = QLineEdit(self)
                self.layout_pemesanan.addWidget(self.kursi_input)

                # Pilihan metode pembayaran
                self.layout_pemesanan.addWidget(QLabel("Pilih Metode Pembayaran:"))
                self.metode_combo = QComboBox(self)
                self.metode_combo.addItems(["Cash", "Debit", "Credit", "E-wallet"])
                self.layout_pemesanan.addWidget(self.metode_combo)

                # Tombol Pemesanan
                self.pesan_button = QPushButton("Pesan", self)
                self.pesan_button.clicked.connect(self.pesan_film)
                self.layout_pemesanan.addWidget(self.pesan_button)

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Gagal mengambil detail film: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()


    def pesan_film(self):
        # Validasi input dan proses pemesanan
        hari_tayang = self.hari_group.checkedButton().text() if self.hari_group.checkedButton() else None
        jam_tayang = self.jam_group.checkedButton().text() if self.jam_group.checkedButton() else None
        kursi = self.kursi_input.text().strip()
        metode_pembayaran = self.metode_combo.currentText()

        if not all([hari_tayang, jam_tayang, kursi, metode_pembayaran]):
            QMessageBox.warning(self, "Pemesanan Gagal", "Pastikan semua data terisi dengan benar.")
            return

        # Proses pemesanan (misalnya menyimpan ke database, dll)
        QMessageBox.information(self, "Pemesanan Berhasil", "Pemesanan Anda berhasil!")

# Main program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = login()
    window.show()
    sys.exit(app.exec_())
