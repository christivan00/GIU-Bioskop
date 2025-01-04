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
            query = "SELECT id, nama_film, harga, durasi, genre, gambar_film FROM film"
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
        layout = QVBoxLayout()

        # Ambil data film berdasarkan id
        self.get_film_detail()

        self.setLayout(layout)
        self.setWindowTitle("Pemesanan Film")
        self.resize(400, 600)

    def get_film_detail(self):
        try:
            connection = self.koneksi_database()
            cursor = connection.cursor()
            query = f"SELECT nama_film, harga, durasi, genre FROM film WHERE id = {self.id_film}"
            cursor.execute(query)
            film = cursor.fetchone()

            if film:
                nama_film, harga, durasi, genre = film

                # Menampilkan detail film
                layout = self.layout()
                layout.addWidget(QLabel(f"Nama Film: {nama_film}"))
                layout.addWidget(QLabel(f"Durasi: {durasi}"))
                layout.addWidget(QLabel(f"Genre: {genre}"))
                layout.addWidget(QLabel(f"Harga: {harga}"))

                # Menambahkan radio button untuk pilihan hari tayang
                layout.addWidget(QLabel("Pilih Hari Tayang:"))
                self.hari_group = QButtonGroup()
                hari_options = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
                for i, day in enumerate(hari_options):
                    radio_button = QRadioButton(day)
                    self.hari_group.addButton(radio_button)
                    layout.addWidget(radio_button)

                # Menambahkan radio button untuk jam tayang
                layout.addWidget(QLabel("Pilih Jam Tayang:"))
                self.jam_group = QButtonGroup()
                jam_options = ["10:00", "13:00", "16:00", "19:00"]
                for i, jam in enumerate(jam_options):
                    radio_button = QRadioButton(jam)
                    self.jam_group.addButton(radio_button)
                    layout.addWidget(radio_button)

                # Input nomor kursi
                layout.addWidget(QLabel("Masukkan Nomor Kursi:"))
                self.kursi_input = QLineEdit(self)
                layout.addWidget(self.kursi_input)

                # Pilihan metode pembayaran
                layout.addWidget(QLabel("Pilih Metode Pembayaran:"))
                self.metode_combo = QComboBox(self)
                self.metode_combo.addItems(["Cash", "Debit", "Credit", "E-wallet"])
                layout.addWidget(self.metode_combo)

                # Tombol Pemesanan
                self.pesan_button = QPushButton("Pesan", self)
                self.pesan_button.clicked.connect(self.pesan_film)
                layout.addWidget(self.pesan_button)

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
