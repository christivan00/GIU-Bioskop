import sys
import qrcode
import mysql.connector
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout,QComboBox,QButtonGroup,QRadioButton,QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from io import BytesIO



class login(QWidget):
    def __init__(self):
        super().__init__()
        self.login_ui()

    def login_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 50, 20, 200)

        # Set Ubuntu font globally
        self.setStyleSheet("font-family: 'Ubuntu';")

        # QLineEdit untuk nama
        self.nama_login = QLineEdit(self)
        self.nama_login.setPlaceholderText("Masukkan nama")
        self.nama_login.setStyleSheet("font-size: 14px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

        # QLineEdit untuk no hp
        self.hp_login = QLineEdit(self)
        self.hp_login.setPlaceholderText("Masukkan no hp")
        self.hp_login.setStyleSheet("font-size: 14px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

        # QLineEdit untuk email
        self.email_login = QLineEdit(self)
        self.email_login.setPlaceholderText("Masukkan email")
        self.email_login.setStyleSheet("font-size: 14px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

        # QLineEdit untuk password
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Masukkan Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("font-size: 14px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

        # Tombol login
        self.tombol_login = QPushButton("Login")
        self.tombol_login.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.tombol_login.clicked.connect(self.next_login)

        # Tombol daftar
        self.tombol_daftar = QPushButton("Daftar")
        self.tombol_daftar.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: #2196F3;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.tombol_daftar.clicked.connect(self.next_daftar)

        # Susunan layout
        label1 = QLabel("BIOSKOP NUSANTARA\n\n")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("""color: #2a3132; font-size: 18px; font-weight: bold; font-family: 'Ubuntu';""")

        label2 = QLabel("Silakan login terlebih dahulu sebelum melakukan pemesanan")
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet("font-size: 14px; color: #555555;")

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
        self.setStyleSheet("background-color: #f0f0f0;")
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
        layout.setContentsMargins(20, 50, 20, 200)

        # Label akun di bagian atas
        label_akun = QLabel(f"Akun: {self.nama_user}")
        label_akun.setAlignment(Qt.AlignLeft)
        label_akun.setStyleSheet("font-size: 14px; font-weight: bold; color: #2a3132; margin: 10px;")
        layout.addWidget(label_akun)

        # Label judul
        label1 = QLabel("Daftar Film")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("font-size: 18px; font-weight: bold; color: #2a3132;")
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
                pixmap = pixmap.scaled(120, 200, Qt.KeepAspectRatio)
                
                # Membuat label untuk gambar film
                image_label = QLabel(self)
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignCenter)
                image_label.setStyleSheet("border: 1px solid #ccc; border-radius: 8px; padding: 5px; margin: 10px;")
                image_label.mousePressEvent = lambda event, id_film=id_film: self.open_pemesanan(id_film)  # Fungsi click

                name_label = QLabel(nama_film)
                name_label.setAlignment(Qt.AlignCenter)
                name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2a3132;")

                price_label = QLabel(f"Harga: {harga}")
                price_label.setAlignment(Qt.AlignCenter)
                price_label.setStyleSheet("font-size: 12px; color: #4CAF50; margin-bottom: 10px;")

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
        self.pemesanan = pemesanan(id_film)
        self.pemesanan.show()
        self.close()



class pemesanan(QWidget):
    def __init__(self, id_film):
        super().__init__()
        self.id_film = id_film  
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
                label1 = QLabel((f"{nama_film}"))
                label1.setAlignment(Qt.AlignCenter)
                label1.setStyleSheet("""color: #2a3132; font-size: 18px; font-weight: bold; font-family: ubuntu;""")
                self.layout_pemesanan.addWidget(label1)
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
        hari_tayang = self.hari_group.checkedButton().text() if self.hari_group.checkedButton() else None
        jam_tayang = self.jam_group.checkedButton().text() if self.jam_group.checkedButton() else None
        kursi = self.kursi_input.text().strip()
        metode_pembayaran = self.metode_combo.currentText()

        if not all([hari_tayang, jam_tayang, kursi, metode_pembayaran]):
            QMessageBox.warning(self, "Pemesanan Gagal", "Pastikan semua data terisi dengan benar.")
            return
        # Proses pemesanan (misalnya menyimpan ke database, dll)
        QMessageBox.information(self, "Pemesanan Berhasil", "Pemesanan Anda berhasil!")
        self.tiket_open = tiket(self.id_film, hari_tayang, jam_tayang, kursi, metode_pembayaran)
        self.tiket_open.show()
        self.close()


class tiket(QWidget):
    def __init__(self, id_film, hari_tayang, jam_tayang, kursi, metode_pembayaran):
        super().__init__()
        self.id_film = id_film
        self.hari_tayang = hari_tayang
        self.jam_tayang = jam_tayang
        self.kursi = kursi
        self.metode_pembayaran = metode_pembayaran
        self.tiket_ui()

    def koneksi_database(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='uas_bioskop'
        )

    def tiket_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)
        self.resize(400, 600)

        # Ambil detail film dari database
        film_detail = self.get_film_detail()

        if film_detail:
            nama_film, harga, durasi, genre = film_detail

            # Header
            label_header = QLabel("Tiket Pemesanan")
            label_header.setAlignment(Qt.AlignCenter)
            label_header.setStyleSheet("font-size: 22px; font-weight: bold; color: #4CAF50;")
            layout.addWidget(label_header)

            # Detail Tiket
            detail_labels = [
                f"Nama Film: {nama_film}",
                f"Durasi: {durasi}",
                f"Harga Tiket: {harga}",
                f"No. Kursi: {self.kursi}",
                f"Metode Pembayaran: {self.metode_pembayaran}"
            ]

            for detail in detail_labels:
                label = QLabel(detail)
                label.setAlignment(Qt.AlignLeft)
                label.setStyleSheet("font-size: 14px; color: #333333; margin: 5px 0;")
                layout.addWidget(label)

            # Buat QR Code
            qr_code_label = QLabel(self)
            qr_code_label.setAlignment(Qt.AlignCenter)
            qr_pixmap = self.generate_qr_code(
                nama_film, self.hari_tayang, self.jam_tayang, self.kursi
            )
            qr_code_label.setPixmap(qr_pixmap)
            layout.addWidget(qr_code_label)

            # Tombol tutup
            button_layout = QHBoxLayout()
            back_button = QPushButton("Tutup")
            back_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 16px;
                    border-radius: 5px;
                    padding: 10px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            back_button.clicked.connect(self.go_back)
            button_layout.addWidget(back_button)
            layout.addLayout(button_layout)

        else:
            QMessageBox.critical(self, "Error", "Gagal memuat detail tiket.")

        self.setLayout(layout)
        self.setWindowTitle("Tiket")
        self.setFixedSize(400, 600)

    def get_film_detail(self):
        try:
            connection = self.koneksi_database()
            cursor = connection.cursor()
            query = f"SELECT nama_film, harga, durasi, genre FROM film WHERE id_film = {self.id_film}"
            cursor.execute(query)
            return cursor.fetchone()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Gagal mengambil data film: {e}")
            return None
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def generate_qr_code(self, nama_film, hari_tayang, jam_tayang, kursi):
        data = f"Film: {nama_film}\nHari: {hari_tayang}\nJam: {jam_tayang}\nKursi: {kursi}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        pixmap = QPixmap()
        pixmap.loadFromData(buffer.read(), "PNG")
        return pixmap

    def go_back(self):
        self.close()

        
# Main program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = login()
    window.show()
    sys.exit(app.exec_())
