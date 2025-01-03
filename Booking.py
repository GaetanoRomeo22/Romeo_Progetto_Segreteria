from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget


class BookingPage(QMainWindow): # Finestra di prenotazione degli appelli
    def __init__(self):
        super().__init__()

        # Finestra
        self.setWindowTitle("Prenotazione Appelli")  # Titolo della finestra
        self.setFixedSize(800, 600)  # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica")  # Stile della finestra

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Allineamento al centro di ogni widget
        self.layout.setSpacing(20)  # Spaziatura tra i widget
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)