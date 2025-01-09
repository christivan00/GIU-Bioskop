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
        self.setStyleSheet("font-family: 'Ubuntu';")

        self.nama_login = QLineEdit(self)
        self.nama_login.setPlaceholderText("Masukkan nama")
        self.nama_login.setStyleSheet("font-size: 14px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

        self.hp_login = QLineEdit(self)
        self.hp_login.setPlaceholderText("Masukkan no hp")
        self.hp_login.setStyleSheet("font-size: 14px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

        self.email_login = QLineEdit(self)
        self.email_login.setPlaceholderText("Masukkan email")
        self.email_login.setStyleSheet("font-size: 14px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Masukkan Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("font-size: 14px; padding: 10px; border-radius: 5px; border: 1px solid #ccc;")

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
        nama = self.nama_login.text().strip()
        no_hp = self.hp_login.text().strip()
        email = self.email_login.text().strip()
        password = self.password.text().strip()

        if not nama or not no_hp or not email or not password:
            QMessageBox.warning(self, "Login Gagal", "Silakan isi email dan password.")
            return

        try:
            connection = self.koneksi_database()
            cursor = connection.cursor()
            query = "SELECT * FROM customer WHERE nama = %s AND no_hp = %s AND email = %s AND password = %s"
            cursor.execute(query, (nama , no_hp,email, password))
            result = cursor.fetchone()

            if result:
                id_cs, nama_user, email_user, hp_user, password_user = result
                QMessageBox.information(self, "Berhasil", "Login berhasil!")
                self.daftar_film = daftar_film(nama_user, hp_user, email_user, password_user)
                self.daftar_film.show()
                self.close()
            else:
                QMessageBox.warning(self, "Login Gagal", "data yang di masukkan salah.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Gagal login: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()



class daftar_film(QWidget):
    def __init__(self, nama_user, hp_user, email_user, password_user):
        super().__init__()
        self.nama_user = nama_user
        self.hp_user = hp_user
        self.email_user = email_user
        self.password_user = password_user
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
        layout.setContentsMargins(20, 50, 20, 100)
        self.setStyleSheet("font-family: 'Ubuntu';")

        label_akun = QLabel(f"User: {self.nama_user}")
        label_akun.setAlignment(Qt.AlignLeft)
        label_akun.setStyleSheet("font-size: 14px; color: #555; margin-bottom: 10px;")
        layout.addWidget(label_akun)

        tombol_Akun = QPushButton("Akun")
        tombol_Akun.setStyleSheet("""
        QPushButton {
            font-size: 14px;
            padding: 8px;
            background-color: #FFC107;
            color: black;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #FFB300;
        }
        """)

        tombol_Akun.clicked.connect(self.info_akun)
        layout.addWidget(tombol_Akun)


        label1 = QLabel("Daftar Film")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("font-size: 18px; font-weight: bold; color: #2a3132;")
        layout.addWidget(label1)

        self.gridLayout = QGridLayout()
        layout.addLayout(self.gridLayout)

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
                gambar_path = gambar_path.replace('/', '\\')  
                pixmap = QPixmap(gambar_path)
                pixmap = pixmap.scaled(120, 200, Qt.KeepAspectRatio)
                
                image_label = QLabel(self)
                image_label.setPixmap(pixmap)
                image_label.setAlignment(Qt.AlignCenter)
                image_label.setStyleSheet("border: 1px solid #ccc; border-radius: 8px; padding: 5px; margin: 10px;")
                image_label.mousePressEvent = lambda event, id_film=id_film: self.open_pemesanan(id_film) 

                name_label = QLabel(nama_film)
                name_label.setAlignment(Qt.AlignCenter)
                name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2a3132;")

                price_label = QLabel(f"Harga: {harga}")
                price_label.setAlignment(Qt.AlignCenter)
                price_label.setStyleSheet("font-size: 12px; color: #4CAF50; margin-bottom: 10px;")

                self.gridLayout.addWidget(name_label, row, col)
                self.gridLayout.addWidget(image_label, row + 1, col)
                self.gridLayout.addWidget(price_label, row + 2, col)

                col += 1
                if col > 1: 
                    col = 0
                    row += 3

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Gagal mengambil data film: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def info_akun(self):
        self.akun = informasi_akun(self.nama_user, self.hp_user, self.email_user, self.password_user)
        self.akun.show()
        self.close()
    


    def open_pemesanan(self, id_film):
        self.pemesanan = pemesanan(id_film)
        self.pemesanan.show()
        self.close()

        
class informasi_akun(QWidget):
    def __init__(self, nama_user, hp_user, email_user, password_user):
        super().__init__()
        self.nama_user = nama_user
        self.hp_user = hp_user
        self.email_user = email_user
        self.password_user = password_user
        self.akun_ui()

    
    def akun_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 50, 20, 200)
        self.setWindowTitle('Info Akun')
        self.setStyleSheet("font-family: 'Ubuntu'; background-color: #f0f0f0;")

        label1 = QLabel("DETAIL AKUN\n\n")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("color: #2a3132; font-size: 18px; font-weight: bold;")
        layout.addWidget(label1)
        
        self.tombol_kembali = QPushButton("kembali")
        self.tombol_kembali.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.tombol_kembali.clicked.connect(self.kembali_ke_daftar_film)  
        layout.addWidget(self.tombol_kembali)
        
        self.tombol_edit = QPushButton("edit akun")
        self.tombol_edit.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.tombol_edit.clicked.connect(self.edit_akun)  
        self.tombol_logout = QPushButton("logout")
        self.tombol_logout.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.tombol_logout.clicked.connect(self.logout)

        self.tombol_hapus_akun = QPushButton("hapus akun")
        self.tombol_hapus_akun.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;`
            }
        """)
        self.tombol_hapus_akun.clicked.connect(self.hapus_akun)  

        layout.addWidget(QLabel(f"Nama: {self.nama_user}"))
        layout.addWidget(QLabel(f"No HP: {self.hp_user}"))
        layout.addWidget(QLabel(f"Email: {self.email_user}"))
        layout.addWidget(QLabel(f"Password: {self.password_user}"))
        layout.addWidget(self.tombol_edit)
        layout.addWidget(self.tombol_logout)
        layout.addWidget(self.tombol_hapus_akun)
        self.setLayout(layout)
        self.resize(400, 600)

            
    def koneksi_database(self):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='uas_bioskop'
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
    def kembali_ke_daftar_film(self):
        self.daftar_film = daftar_film(self.nama_user, self.hp_user, self.email_user, self.password_user)
        self.daftar_film.show()
        self.close()
        
    def edit_akun(self):
        self.edit_form = EditAkun(self.nama_user, self.hp_user, self.email_user, self.password_user)
        self.edit_form.show()
        self.close()
        
    def logout(self):
        QMessageBox.information(self, "Logout", "Anda telah logout.")
        self.login = login()
        self.login.show()
        self.close()

    def hapus_akun(self):
        reply = QMessageBox.question(self, 'Hapus Akun', 
                                    "Apakah Anda yakin ingin menghapus akun ini? Semua data akan hilang.",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.proses_hapus_akun()

    def proses_hapus_akun(self):
        try:
            connection = self.koneksi_database()
            cursor = connection.cursor()
            query = "DELETE FROM customer WHERE email = %s"
            cursor.execute(query, (self.email_user,))
            connection.commit()

            QMessageBox.information(self, "Akun Dihapus", "Akun Anda telah berhasil dihapus.")
            
            self.login = login() 
            self.login.show()
            self.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Gagal menghapus akun: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

        
class EditAkun(QWidget):
    def __init__(self, nama_user, hp_user, email_user, password_user):
        super().__init__()
        self.nama_user = nama_user
        self.hp_user = hp_user
        self.email_user = email_user
        self.password_user = password_user
        self.edit_akun_ui()

    def edit_akun_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 50, 20, 100)
        self.setWindowTitle('Edit Akun')
        self.setStyleSheet("font-family: 'Ubuntu'; background-color: #f0f0f0;")

        label1 = QLabel("EDIT AKUN\n\n")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("color: #2a3132; font-size: 18px; font-weight: bold;")
        layout.addWidget(label1)

        # Input untuk Nama
        self.nama_edit = QLineEdit(self)
        self.nama_edit.setText(self.nama_user)
        self.nama_edit.setPlaceholderText("Nama")
        layout.addWidget(QLabel("nama"))
        layout.addWidget(self.nama_edit)

        # Input untuk No HP
        self.hp_edit = QLineEdit(self)
        self.hp_edit.setText(self.hp_user)
        self.hp_edit.setPlaceholderText("No HP")
        layout.addWidget(QLabel("No HP"))
        layout.addWidget(self.hp_edit)

        # Input untuk Email
        self.email_edit = QLineEdit(self)
        self.email_edit.setText(self.email_user)
        self.email_edit.setPlaceholderText("Email")
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_edit)

        # Input untuk Password
        self.password_edit = QLineEdit(self)
        self.password_edit.setText(self.password_user)
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_edit)

        tombol_simpan = QPushButton("Simpan Perubahan")
        tombol_simpan.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 8px;
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        tombol_simpan.clicked.connect(self.simpan_perubahan) 
        layout.addWidget(tombol_simpan)

        self.setLayout(layout)
        self.resize(400, 600)

    def simpan_perubahan(self):
        # Mengambil data yang telah diedit
        nama_baru = self.nama_edit.text().strip()
        hp_baru = self.hp_edit.text().strip()
        email_baru = self.email_edit.text().strip()
        password_baru = self.password_edit.text().strip()

        # Validasi input
        if not nama_baru or not hp_baru or not email_baru or not password_baru:
            QMessageBox.warning(self, "Edit Gagal", "Silakan isi semua data.")
            return

        try:
            connection = self.koneksi_database()
            cursor = connection.cursor()
            query = "UPDATE customer SET nama = %s, no_hp = %s, email = %s, password = %s WHERE email = %s"
            cursor.execute(query, (nama_baru, hp_baru, email_baru, password_baru, self.email_user))
            connection.commit()

            QMessageBox.information(self, "Berhasil", "Akun berhasil diperbarui.")
            
            # Setelah menyimpan perubahan, kembali ke halaman info akun
            self.info_akun = informasi_akun(nama_baru, hp_baru, email_baru, password_baru)
            self.info_akun.show()
            self.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Gagal memperbarui akun: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def koneksi_database(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='uas_bioskop'
        )

            

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
        self.layout_pemesanan = QVBoxLayout()
        self.layout_pemesanan.setContentsMargins(20, 10, 20, 200)
        self.setStyleSheet("font-family: 'Ubuntu';")

        self.get_film_detail()

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

                label1 = QLabel((f"{nama_film}"))
                label1.setAlignment(Qt.AlignCenter)
                label1.setStyleSheet("""color: #2a3132; font-size: 18px; font-weight: bold; font-family: ubuntu;""")
                self.layout_pemesanan.addWidget(label1)
                self.layout_pemesanan.addWidget(QLabel(f"Durasi: {durasi}"))
                self.layout_pemesanan.addWidget(QLabel(f"Genre: {genre}"))
                self.layout_pemesanan.addWidget(QLabel(f"Harga: {harga}"))
                
                labebatas = QLabel(f"_"*50)
                labebatas.setAlignment(Qt.AlignCenter)
                self.layout_pemesanan.addWidget(labebatas)

                self.layout_pemesanan.addWidget(QLabel("Pilih Hari Tayang:"))
                self.hari_group = QButtonGroup()
                hari_options = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
                
                hari_layout = QHBoxLayout()
                for day in hari_options:
                    radio_button = QRadioButton(day)
                    self.hari_group.addButton(radio_button)
                    hari_layout.addWidget(radio_button)
                self.layout_pemesanan.addLayout(hari_layout)

                self.layout_pemesanan.addWidget(QLabel("Pilih Jam Tayang:"))
                self.jam_group = QButtonGroup()
                jam_options = ["10:00", "13:00", "16:00", "19:00"]
                
                jam_layout = QHBoxLayout()
                for jam in jam_options:
                    radio_button = QRadioButton(jam)
                    self.jam_group.addButton(radio_button)
                    jam_layout.addWidget(radio_button)
                self.layout_pemesanan.addLayout(jam_layout)

                self.layout_pemesanan.addWidget(QLabel("Masukkan Nomor Kursi:"))
                self.kursi_input = QLineEdit(self)
                self.layout_pemesanan.addWidget(self.kursi_input)

                self.layout_pemesanan.addWidget(QLabel("Pilih Metode Pembayaran:"))
                self.metode_combo = QComboBox(self)
                self.metode_combo.addItems(["Cash", "Debit", "Credit", "E-wallet"])
                self.layout_pemesanan.addWidget(self.metode_combo)

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

        film_detail = self.get_film_detail()

        if film_detail:
            nama_film, harga, durasi, genre = film_detail

            label_header = QLabel("TIKET NUSANTARA")
            label_header.setAlignment(Qt.AlignCenter)
            label_header.setStyleSheet("font-size: 22px; font-weight: bold; color: #4CAF50;")
            layout.addWidget(label_header)

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

            qr_code_label = QLabel(self)
            qr_code_label.setAlignment(Qt.AlignCenter)
            qr_pixmap = self.generate_qr_code(
                nama_film, self.hari_tayang, self.jam_tayang, self.kursi
            )
            qr_code_label.setPixmap(qr_pixmap)
            layout.addWidget(qr_code_label)

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
        qr = qrcode.QRCode(version=1, box_size=6, border=5)
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



        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = login()
    window.show()
    sys.exit(app.exec_())
