import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame, QPushButton, QDialog, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import pymysql

# Fungsi untuk menghubungkan ke database
def get_film_data():
    try:
        # Koneksi ke database
        conn = pymysql.connect(host='localhost', user='root', password='', database='uas_bioskop')
        cursor = conn.cursor()

        # Query untuk mengambil data film
        query = "SELECT nama_film, harga, durasi FROM film"
        cursor.execute(query)
        films = cursor.fetchall()  # Menyimpan hasil query ke dalam list

        # Menutup koneksi
        cursor.close()
        conn.close()

        # Mengembalikan data film
        return films
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return []


class DetailFilm(QDialog):
    def __init__(self, judul, deskripsi):
        super().__init__()
        self.setWindowTitle("Detail Film")
        self.resize(400, 300)

        # Layout untuk detail film
        layout = QVBoxLayout()

        # Label judul
        label_judul = QLabel(f"Judul: {judul}")
        label_judul.setStyleSheet("font-weight: bold; font-size: 16px;")
        label_judul.setAlignment(Qt.AlignCenter)

        # Label deskripsi
        label_deskripsi = QLabel(f"Deskripsi: {deskripsi}")
        label_deskripsi.setWordWrap(True)
        label_deskripsi.setAlignment(Qt.AlignCenter)

        # Tambahkan widget ke layout
        layout.addWidget(label_judul)
        layout.addWidget(label_deskripsi)
        self.setLayout(layout)


class FilmGallery(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_film = None  # Untuk menyimpan film yang dipilih
        self.init_ui()

    def init_ui(self):
        # Set judul window
        self.setWindowTitle("Daftar Film")
        self.resize(400, 600)

        # Layout utama
        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Label judul aplikasi
        label1 = QLabel('DAFTAR FILM')
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("font-size: 18px; font-weight: bold;")

        # Ambil data film dari database
        films = get_film_data()

        # Menambahkan film ke dalam grid
        for index, film in enumerate(films):
            frame = QFrame()
            frame_layout = QVBoxLayout()

            # Menambahkan tombol dan gambar film (gambar akan disesuaikan dengan path yang benar)
            pixmap_path = f"gambar/{film[0]}.jpg"
            pixmap = QPixmap(pixmap_path)

            if pixmap.isNull():  # Jika gambar tidak ditemukan
                pixmap = QPixmap(150, 200)  # Placeholder ukuran gambar
                pixmap.fill(Qt.lightGray)

            pixmap = pixmap.scaled(150, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon = QIcon(pixmap)  # Konversi QPixmap ke QIcon
            button = QPushButton()
            button.setIcon(icon)
            button.setIconSize(pixmap.size())
            button.clicked.connect(self.create_film_callback(film))

            # Judul film
            judul_label = QLabel(film[0])  # Nama film
            judul_label.setAlignment(Qt.AlignCenter)
            judul_label.setStyleSheet("font-weight: bold; font-size: 14px;")

            # Menambahkan komponen ke frame
            frame_layout.addWidget(button)
            frame_layout.addWidget(judul_label)
            frame.setLayout(frame_layout)
            frame.setFrameShape(QFrame.StyledPanel)

            # Menempatkan frame ke dalam grid
            row = index // 2  # Maksimal 2 kolom
            col = index % 2
            grid_layout.addWidget(frame, row, col)

        # Tambahkan grid ke layout utama
        main_layout.addWidget(label1)
        main_layout.addLayout(grid_layout)

        # Footer dengan tombol konfirmasi
        footer_layout = QHBoxLayout()
        confirm_button = QPushButton("Konfirmasi Pilihan")
        confirm_button.setStyleSheet("font-size: 14px;")
        confirm_button.clicked.connect(self.confirm_selection)
        footer_layout.addWidget(confirm_button, alignment=Qt.AlignCenter)

        # Tambahkan footer ke layout utama
        main_layout.addLayout(footer_layout)
        self.setLayout(main_layout)

    def create_film_callback(self, film):
        def callback():
            self.select_film(film)
        return callback

    def select_film(self, film):
        # Menyimpan film yang dipilih
        self.selected_film = film
        print(f"Film dipilih: {film[0]}")  # Untuk debugging atau log

    def confirm_selection(self):
        # Menampilkan dialog atau aksi konfirmasi
        if self.selected_film:
            detail_form = DetailFilm(
                self.selected_film[0],  # Nama film
                f"Durasi: {self.selected_film[2]} menit"  # Durasi film
            )
            detail_form.exec_()
        else:
            # Tidak ada film yang dipilih
            no_selection_dialog = QDialog(self)
            no_selection_dialog.setWindowTitle("Peringatan")
            no_selection_dialog.resize(300, 150)
            layout = QVBoxLayout()
            label = QLabel("Anda belum memilih film!")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            no_selection_dialog.setLayout(layout)
            no_selection_dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gallery = FilmGallery()
    gallery.show()
    sys.exit(app.exec_())
