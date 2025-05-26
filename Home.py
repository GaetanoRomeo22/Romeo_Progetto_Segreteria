from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFrame

from Career import CareerPage
from Booking import BookingPage
from NextExams import NextExamsPage


class HomeWindow(QMainWindow):
    def __init__(self, matricola: str, name: str):
        super().__init__()
        self.matricola = matricola # Matricola dello studente loggato
        self.name = name # Nome dello studente loggato

        self.login_page = None # Pagina di login
        self.career_page = None # Pagina di visualizzazione degli esami dati
        self.booking_page = None # Pagina di visualizzazione degli appelli prenotabili
        self.next_exams_page = None # Pagina di visualizzazione degli appelli prenotati

        # Finestra
        self.setWindowTitle("Home")  # Titolo della finestra
        # self.setFixedSize(800, 600)  # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica")  # Stile della finestra
        self.showFullScreen()  # Schermo intero

        # Intestazione
        self.header_label = QLabel(f"Benvenuto {self.name}")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00796b;
            margin-bottom: 20px;
            margin-top: 40px;
        """)

        # Logo
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter)  # Allineamento al centro
        self.pixmap = QPixmap("logo.png")  # Immagine logo
        self.pixmap = self.pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Ridimensiona l'immagine
        self.logo.setPixmap(self.pixmap)
        self.logo.setStyleSheet("""
            margin-bottom: 20px;
            margin-top: 20px;
        """)

        # Pulsante di prenotazione ad un appello
        self.booking_button = QPushButton("Appelli disponibili")
        self.booking_button.setFixedSize(350, 50)  # Dimensioni
        self.booking_button.clicked.connect(self.show_booking_page) # Funzione del bottone

        # Pulsante di visualizzazione prossimi esami
        self.view_button = QPushButton("Appelli prenotati")
        self.view_button.setFixedSize(350, 50)  # Dimensioni
        self.view_button.clicked.connect(self.show_next_exams_page) # Funzione del bottone

        # Pulsante di visualizzazione degli esami dati
        self.career_button = QPushButton("Libretto")
        self.career_button.setFixedSize(350, 50)  # Dimensioni
        self.career_button.clicked.connect(self.show_given_exams_page) # Funzione del bottone

        # Stile dei bottoni
        button_style = """
            QPushButton {
                background-color: #00796b;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #004d40;
            }
            QPushButton:pressed {
                background-color: #00251a;
            }
        """
        self.booking_button.setStyleSheet(button_style)
        self.view_button.setStyleSheet(button_style)
        self.career_button.setStyleSheet(button_style)

        # Pulsante di logout
        self.logout_button = QPushButton("Logout")
        self.logout_button.setFixedSize(350, 50) # Dimensioni
        self.logout_button.clicked.connect(self.logout) # Funzione del bottone
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f;
                color: white;
                border: 2px solid #b71c1c;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPushButton:pressed {
                background-color: #ff6659;
            }
        """)

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
                padding: 20px;
                margin-top: 50px;
            }
            """)
        self.choices_layout = QVBoxLayout()
        self.choices_layout.setAlignment(Qt.AlignCenter)  # Allinea i pulsanti al centro
        self.choices_layout.setSpacing(25)  # Spaziatura tra i pulsanti

        # Aggiungere i pulsanti al layout
        self.choices_layout.addWidget(self.booking_button)
        self.choices_layout.addWidget(self.view_button)
        self.choices_layout.addWidget(self.career_button)
        self.choices_layout.addWidget(self.logout_button)
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

    def show_booking_page(self): # Funzione di visualizzazione della pagina di prenotazione di un appello
        self.close() # Chiude la home page
        self.booking_page = BookingPage(self.matricola, self) # Crea una finestra per la prenotazione di un appello
        self.booking_page.show() # Mostra gli appelli prenotabili

    def show_next_exams_page(self): # Funzione di visualizzazione della pagina degli appelli prenotati
        self.close()  # Chiude la home page
        self.next_exams_page = NextExamsPage(self.matricola, self)  # Crea una finestra per visualizzare gli appelli prenotati
        self.next_exams_page.show()  # Mostra gli appelli prenotati

    def show_given_exams_page(self): # Funzione di visualizzazione degli esami dati dallo studente
        self.close()  # Chiude la home page
        self.career_page = CareerPage(self.matricola, self)  # Crea una finestra per visualizzare gli esami superati
        self.career_page.show()  # Mostra gli esami superati

    def logout(self): # Funzione di logout per l'utente
        from Login import LoginWindow
        self.close() # Chiude la home page
        self.login_page = LoginWindow() # Crea una finestra di login
        self.login_page.show() # Mostra la finestra di login