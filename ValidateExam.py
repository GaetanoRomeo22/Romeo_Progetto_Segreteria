from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton

from DatabaseConnection import connection


class ValidateExamPage(QMainWindow):
    def __init__(self, office_page):
        super().__init__()

        self.office_window = office_page  # Finestra per la pagina della segreteria

        # Finestra
        self.setWindowTitle("Validazione Esame")  # Titolo della finestra
        # self.setFixedSize(800, 600) # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica")  # Stile della finestra
        self.showFullScreen()  # Schermo intero

        # Intestazione
        self.header_label = QLabel("Convalida esami")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00796b;
            margin-bottom: 20px;
            margin-top: 20px;
        """)

        # Pulsante per tornare alla home page
        self.back_button = QPushButton("Esci")
        self.back_button.setFixedSize(300, 40)  # Dimensioni
        self.back_button.clicked.connect(self.show_office_window)  # Funzione del bottone
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border-radius: 10px;
                font-size: 18px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPushButton:pressed {
                background-color: #ff6659;
            }
        """)  # Stile del bottone

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Allineamento al centro di ogni widget
        self.layout.setSpacing(20)  # Spaziatura tra i widget

        # Aggiunta dei widget al layout
        self.layout.insertWidget(0, self.header_label)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

    def show_office_window(self):
        self.close() # Chiude la pagina
        self.office_window.show() # Mostra la pagina della segreteria