from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QFrame, QWidget


class OfficePage(QMainWindow):
    def __init__(self):
        super().__init__()

        # Finestra
        self.setWindowTitle("Segreteria")  # Titolo della finestra
        # self.setFixedSize(800, 600)  # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica")  # Stile della finestra
        self.showFullScreen()  # Schermo intero

        # Intestazione
        self.header_label = QLabel("Segreteria")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #00796b;
            margin-bottom: 10px;
        """)

        # Logo
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter)  # Allineamento al centro
        self.pixmap = QPixmap("uniparthenope.png")  # Immagine logo
        self.pixmap = self.pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Ridimensiona l'immagine
        self.logo.setPixmap(self.pixmap)

        # Pulsante di inserimento di un appello
        self.adding_button = QPushButton("Inserimento Appelli", self)
        self.adding_button.setFixedSize(350, 50)  # Dimensioni
        # self.adding_button.clicked.connect()  # Funzione del bottone

        # Pulsante di convalida degli esami
        self.validate_button = QPushButton("Convalida Esami", self)
        self.validate_button.setFixedSize(350, 50)  # Dimensioni
        # self.validate_button.clicked.connect()  # Funzione del bottone

        # Stile dei bottoni
        button_style = """
            QPushButton {
                background-color: #00796b;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #004d40;
            }
            QPushButton:pressed {
                background-color: #00251a;
            }
        """
        self.adding_button.setStyleSheet(button_style)
        self.validate_button.setStyleSheet(button_style)

        # Layout del logo
        self.logo_layout = QVBoxLayout()
        self.logo_layout.addWidget(self.logo)
        self.logo_layout.setAlignment(Qt.AlignCenter)  # Allinea il logo al centro

        # Layout per i pulsanti
        self.choices_frame = QFrame()  # Widget per contenere i pulsanti
        self.choices_frame.setStyleSheet("""
            QFrame {
                border: 3px solid #00796b;
                border-radius: 15px;
                background-color: #f0f0f0;
                padding: 30px;
                margin-top: 20px;
                box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1);
            }
            QFrame:hover {
                background-color: #e0e0e0;
                box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.2);
            }
        """)
        self.choices_layout = QVBoxLayout()
        self.choices_layout.setAlignment(Qt.AlignCenter)  # Allinea i pulsanti al centro
        self.choices_layout.setSpacing(25)  # Spaziatura tra i pulsanti

        # Aggiungere i pulsanti al layout
        self.choices_layout.addWidget(self.adding_button)
        self.choices_layout.addWidget(self.validate_button)
        self.choices_frame.setLayout(self.choices_layout)

        # Layout principale
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Allineamento generale al centro di tutti i widget
        self.layout.setSpacing(30)  # Spaziatura tra i widget

        # Aggiunta dei widget al layout
        self.layout.insertWidget(0, self.header_label)
        self.layout.addLayout(self.logo_layout)  # Aggiunge il logo
        self.layout.addWidget(self.choices_frame)  # Aggiunge il frame con i pulsanti
        self.layout.addStretch()  # Spazio extra alla fine per centrare gli elementi

        # Impostazione del widget centrale
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)