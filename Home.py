from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from mysql.connector import Error

from Career import CareerPage
from Booking import BookingPage
from NextExams import NextExamsPage
from DatabaseConnection import connection


class HomeWindow(QMainWindow):
    def __init__(self, matricola: str):
        super().__init__()
        self.matricola = matricola # Matricola dello studente loggato

        self.career_page = None # Pagina di visualizzazione degli esami dati
        self.booking_page = None # Pagina di visualizzazione degli appelli prenotabili
        self.next_exams_page = None # Pagina di visualizzazione degli appelli prenotati

        # Finestra
        self.setWindowTitle("Home")  # Titolo della finestra
        self.setFixedSize(800, 600)  # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica")  # Stile della finestra

        # Logo
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter)  # Allineamento al centro
        self.pixmap = QPixmap("uniparthenope.png")  # Immagine logo
        self.pixmap = self.pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Ridimensiona l'immagine
        self.logo.setPixmap(self.pixmap)

        # Pulsante di prenotazione ad un appello
        self.booking_button = QPushButton("Prenotazione appelli", self)
        self.booking_button.setFixedSize(300, 40)  # Dimensioni
        self.booking_button.setStyleSheet("background-color: green; color: white; border-radius: 5px; font-size: 18px")  # Stile del bottone
        self.booking_button.clicked.connect(self.book_exam) # Funzione del bottone

        # Pulsante di visualizzazione prossimi esami
        self.view_button = QPushButton("Visualizzazione prossimi esami", self)
        self.view_button.setFixedSize(300, 40)  # Dimensioni
        self.view_button.setStyleSheet("background-color: green; color: white; border-radius: 5px; font-size: 18px")  # Stile del bottone
        self.view_button.clicked.connect(self.show_next_exams) # Funzione del bottone

        # Pulsante di visualizzazione degli esami dati
        self.career_button = QPushButton("Visualizzazione libretto", self)
        self.career_button.setFixedSize(300, 40)  # Dimensioni
        self.career_button.setStyleSheet("background-color: green; color: white; border-radius: 5px; font-size: 18px")  # Stile del bottone
        self.career_button.clicked.connect(self.show_given_exams) # Funzione del bottone

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Allineamento al centro di ogni widget
        self.layout.setSpacing(20)  # Spaziatura tra i widget
        self.layout.addWidget(self.logo)
        self.layout.addWidget(self.booking_button)
        self.layout.addWidget(self.view_button)
        self.layout.addWidget(self.career_button)
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

    def book_exam(self): # Funzione di prenotazione di un appello per lo studente
        try:
            conn = connection()  # Connessione al database
            cursor = conn.cursor()  # Cursore per la query
            query = ("")  # Query da eseguire
            cursor.execute(query, )  # Esegue la query
            given_exams = cursor.fetchall()  # Risultati della query
            self.close()  # Chiude la home page
            self.booking_page = BookingPage()  # Crea una finestra per visualizzare gli esami superati
            self.booking_page.show()  # Mostra gli appelli prenotabili
        except Error as e:
            print(f"Errore durante la connessione al database: {e}")
        finally:
            if conn.is_connected():
                conn.close()  # Chiude la connessione al database

    def show_next_exams(self): # Funzione di visualizzazione degli appelli prenotati dallo studente
        try:
            conn = connection()  # Connessione al database
            cursor = conn.cursor()  # Cursore per la query
            query = ("SELECT A.DATAESAME, A.NOMEESAME, A.CORSO FROM APPELLI A JOIN PRENOTA P ON A.NOMEESAME = P.NOMEESAME"
                     " AND A.CORSO = P.CORSO WHERE P.MATRICOLA = %s")  # Query da eseguire
            cursor.execute(query, (self.matricola, ))  # Esegue la query
            next_exams = cursor.fetchall()  # Risultati della query
            self.close()  # Chiude la home page
            self.next_exams_page = NextExamsPage(next_exams)  # Crea una finestra per visualizzare gli esami superati
            self.next_exams_page.show()  # Mostra gli appelli prenotati
        except Error as e:
            print(f"Errore durante la connessione al database: {e}")
        finally:
            if conn.is_connected():
                conn.close()  # Chiude la connessione al database

    def show_given_exams(self): # Funzione di visualizzazione degli esami dati dallo studente
        try:
            conn = connection() # Connessione al database
            cursor = conn.cursor()  # Cursore per la query
            query = ("SELECT A.NOMEESAME, A.CORSO, SP.VOTO, A.DATAESAME FROM SUPERA SP "
                     " JOIN APPELLI A ON SP.NOMEESAME = A.NOMEESAME AND SP.CORSO = A.CORSO WHERE SP.MATRICOLA = %s")  # Query da eseguire
            cursor.execute(query, (self.matricola, )) # Esegue la query
            given_exams = cursor.fetchall()  # Risultati della query
            self.close() # Chiude la home page
            self.career_page = CareerPage(given_exams) # Crea una finestra per visualizzare gli esami superati
            self.career_page.show() # Mostra gli esami superati
        except Error as e:
            print(f"Errore durante la connessione al database: {e}")
        finally:
            if conn.is_connected():
                conn.close()  # Chiude la connessione al database