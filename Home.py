from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QFrame
from mysql.connector import Error
from datetime import datetime

from Career import CareerPage
from Booking import BookingPage
from NextExams import NextExamsPage
from DatabaseConnection import connection


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
            margin-top: 20px;
        """)

        # Logo
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter)  # Allineamento al centro
        self.pixmap = QPixmap("uniparthenope.png")  # Immagine logo
        self.pixmap = self.pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Ridimensiona l'immagine
        self.logo.setPixmap(self.pixmap)

        # Pulsante di prenotazione ad un appello
        self.booking_button = QPushButton("Prenotazione appelli")
        self.booking_button.setFixedSize(350, 50)  # Dimensioni
        self.booking_button.clicked.connect(self.book_exam) # Funzione del bottone

        # Pulsante di visualizzazione prossimi esami
        self.view_button = QPushButton("Visualizzazione prossimi esami")
        self.view_button.setFixedSize(350, 50)  # Dimensioni
        self.view_button.clicked.connect(self.show_next_exams) # Funzione del bottone

        # Pulsante di visualizzazione degli esami dati
        self.career_button = QPushButton("Visualizzazione libretto")
        self.career_button.setFixedSize(350, 50)  # Dimensioni
        self.career_button.clicked.connect(self.show_given_exams) # Funzione del bottone

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
                margin-top: 20px;
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

    def book_exam(self): # Funzione di prenotazione di un appello per lo studente
        try:
            conn = connection()  # Connessione al database
            cursor = conn.cursor()  # Cursore per la query
            query = "SELECT CORSOSTUDENTE FROM STUDENTI WHERE MATRICOLA = %s" # Query per estrapolare il corso dello studente
            cursor.execute(query, (self.matricola, )) # Esegue la query
            student_course = cursor.fetchone() # Salva il risultato
            query = ("SELECT NOMEESAME, NOMECORSO, DATAESAME FROM APPELLI"
                     " WHERE NOMECORSO = %s AND DATAESAME > %s") # Query per estrapolare gli appelli prenotabili
            current_date = datetime.now().date() # Data corrente
            cursor.execute(query, (student_course[0], current_date)) # Esegue la query
            available_exams = cursor.fetchall() # Risultati della query
            self.close()  # Chiude la home page
            self.booking_page = BookingPage(available_exams, self)  # Crea una finestra per visualizzare gli esami superati
            self.booking_page.show()  # Mostra gli appelli prenotabili
        except Error as e:
            print(f"Errore durante la connessione al database: {e}")
        finally:
            if conn.is_connected():
                cursor.close()  # Chiude il cursore
                conn.close()  # Chiude la connessione al database

    def show_next_exams(self): # Funzione di visualizzazione degli appelli prenotati dallo studente
        try:
            conn = connection()  # Connessione al database
            cursor = conn.cursor()  # Cursore per la query
            query = ("SELECT A.NOMEESAME, A.NOMECORSO, A.DATAESAME FROM APPELLI A JOIN PRENOTA P ON A.NOMEESAME = P.NOMEESAME"
                     " AND A.NOMECORSO = P.NOMECORSO WHERE P.MATRICOLA = %s AND A.DATAESAME > %s")  # Query da eseguire
            current_date = datetime.now().date()  # Data corrente
            cursor.execute(query, (self.matricola, current_date))  # Esegue la query
            next_exams = cursor.fetchall()  # Risultati della query
            self.close()  # Chiude la home page
            self.next_exams_page = NextExamsPage(next_exams, self)  # Crea una finestra per visualizzare gli esami superati
            self.next_exams_page.show()  # Mostra gli appelli prenotati
        except Error as e:
            print(f"Errore durante la connessione al database: {e}")
        finally:
            if conn.is_connected():
                cursor.close()  # Chiude il cursore
                conn.close()  # Chiude la connessione al database

    def show_given_exams(self): # Funzione di visualizzazione degli esami dati dallo studente
        try:
            conn = connection() # Connessione al database
            cursor = conn.cursor()  # Cursore per la query
            query = ("SELECT A.NOMEESAME, A.NOMECORSO, SP.VOTO, A.DATAESAME FROM SUPERA SP "
                     " JOIN APPELLI A ON SP.NOMEESAME = A.NOMEESAME AND SP.NOMECORSO = A.NOMECORSO WHERE SP.MATRICOLA = %s")  # Query da eseguire
            cursor.execute(query, (self.matricola, )) # Esegue la query
            given_exams = cursor.fetchall()  # Risultati della query
            self.close() # Chiude la home page
            self.career_page = CareerPage(given_exams, self) # Crea una finestra per visualizzare gli esami superati
            self.career_page.show() # Mostra gli esami superati
        except Error as e:
            print(f"Errore durante la connessione al database: {e}")
        finally:
            if conn.is_connected():
                cursor.close()  # Chiude il cursore
                conn.close()  # Chiude la connessione al database

    def logout(self): # Funzione di logout per l'utente
        from Login import LoginWindow
        self.close() # Chiude la home page
        self.login_page = LoginWindow() # Crea una finestra di login
        self.login_page.show() # Mostra la finestra di login