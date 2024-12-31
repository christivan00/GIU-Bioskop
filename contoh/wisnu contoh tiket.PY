import sys
import qrcode
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QMessageBox, QDialog, QFormLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from io import BytesIO

class FilmTicket(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Tiket Film")
        self.resize(400, 350)

        # Layout Utama
        main_layout = QVBoxLayout()

        # Judul Film
        movie_layout = QHBoxLayout()
        movie_label = QLabel("Judul Film:")
        self.movie_input = QLineEdit()
        movie_layout.addWidget(movie_label)
        movie_layout.addWidget(self.movie_input)

        # Tahun Film (Format Tahun Saja)
        year_layout = QHBoxLayout()
        year_label = QLabel("Tahun (YYYY):")
        self.year_input = QLineEdit()
        year_layout.addWidget(year_label)
        year_layout.addWidget(self.year_input)

        # Durasi Film (Dalam Menit)
        time_layout = QHBoxLayout()
        time_label = QLabel("Durasi (menit):")
        self.time_input = QLineEdit()
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_input)

        # Nomor Kursi
        seat_layout = QHBoxLayout()
        seat_label = QLabel("Nomor Kursi:")
        self.seat_input = QLineEdit()
        seat_layout.addWidget(seat_label)
        seat_layout.addWidget(self.seat_input)

        # Tombol untuk Membuat Tiket
        self.generate_button = QPushButton("Buat")
        self.generate_button.clicked.connect(self.generate_ticket)

        # Menambahkan ke Layout
        main_layout.addLayout(movie_layout)
        main_layout.addLayout(year_layout)
        main_layout.addLayout(time_layout)
        main_layout.addLayout(seat_layout)
        main_layout.addWidget(self.generate_button)

        self.setLayout(main_layout)
    
    def generate_ticket(self):
        # Mengambil input dari pengguna
        movie_title = self.movie_input.text()
        movie_year = self.year_input.text()
        movie_duration = self.time_input.text()
        seat_number = self.seat_input.text()

        # Validasi input
        if not movie_title or not movie_year or not movie_duration or not seat_number:
            QMessageBox.warning(self, "Kesalahan Input", "Harap isi semua kolom!")
            return
        
        # Memeriksa apakah tahun dan durasi valid
        if not movie_year.isdigit() or len(movie_year) != 4:
            QMessageBox.warning(self, "Kesalahan Input", "Harap masukkan tahun yang valid (YYYY).")
            return

        if not movie_duration.isdigit() or int(movie_duration) <= 0:
            QMessageBox.warning(self, "Kesalahan Input", "Harap masukkan durasi film yang valid dalam menit.")
            return

        # Membuat string informasi tiket
        ticket_info = f"Film: {movie_title}\nTahun: {movie_year}\nDurasi: {movie_duration} menit\nKursi: {seat_number}"

        # Membuat QR code dari informasi tiket
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(ticket_info)
        qr.make(fit=True)

        # Membuat gambar dari QR code
        img = qr.make_image(fill="black", back_color="white")

        # Mengonversi gambar ke QPixmap
        byte_array = BytesIO()
        img.save(byte_array)
        byte_array.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array.read())

        # Menampilkan detail tiket dalam dialog baru
        ticket_dialog = QDialog(self)
        ticket_dialog.setWindowTitle("Tiket")
        ticket_dialog.resize(400, 350)

        ticket_layout = QVBoxLayout()

        # Membuat layout form untuk menampilkan detail tiket
        form_layout = QFormLayout()

        # Menambahkan informasi tiket ke layout form
        form_layout.addRow("Judul Film:", QLabel(movie_title))
        form_layout.addRow("Durasi (menit):", QLabel(movie_duration))
        form_layout.addRow("Nomor Kursi:", QLabel(seat_number))

        ticket_layout.addLayout(form_layout)

        # Menambahkan gambar QR code ke dialog
        qr_code_label = QLabel()
        qr_code_label.setPixmap(pixmap)
        qr_code_label.setAlignment(Qt.AlignCenter)

        ticket_layout.addWidget(qr_code_label)

        ticket_dialog.setLayout(ticket_layout)
        ticket_dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FilmTicket()
    window.show()
    sys.exit(app.exec_())
