from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QDateEdit, QComboBox
from mysql.connector import Error

from DatabaseConnection import connection


class AddExamPage(QMainWindow):
    def __init__(self, office_page):
        super().__init__()

        self.office_window = office_page  # Finestra per la pagina della segreteria

        # Finestra
        self.setWindowTitle("Inserimento Appello")  # Titolo della finestra
        # self.setFixedSize(800, 600) # Dimensioni della finestra
        self.setStyleSheet("background-color: #f5f5f5; font-family: Helvetica")  # Stile della finestra
        self.showFullScreen()  # Schermo intero

        # Intestazione
        self.header_label = QLabel("Aggiungi un nuovo appello")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00796b;
            margin-bottom: 20px;
            margin-top: 20px;
        """)

        # Nome dell'esame
        self.exam_name_label = QLabel("Nome esame")  # Etichetta per il nome dell'esame
        self.exam_name_label.setStyleSheet("color: #333; font-size: 18px; font-weight: bold;")
        self.exam_name = QComboBox()  # Menu a tendina per i nomi degli esami
        self.exam_name.setFixedSize(300, 40)  # Dimensioni del menu
        self.exam_name.setStyleSheet("""
            QComboBox {
                background-color: #f7f7f7;
                color: black;
                font-size: 16px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QComboBox:focus {
                border: 1px solid #00aaff;
                background-color: #ffffff;
            }
        """)

        # Nome dell'esame
        self.exam_course_label = QLabel("Nome corso")  # Etichetta per il nome dell'esame
        self.exam_course_label.setStyleSheet("color: #333; font-size: 18px; font-weight: bold;")
        self.exam_course = QComboBox()  # Menu a tendina per i nomi degli esami
        self.exam_course.setFixedSize(300, 40)  # Dimensioni del menu
        self.exam_course.setStyleSheet("""
            QComboBox {
                background-color: #f7f7f7;
                color: black;
                font-size: 16px;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QComboBox:focus {
                border: 1px solid #00aaff;
                background-color: #ffffff;
            }
        """)

        # Data dell'appello
        self.exam_date_label = QLabel("Data appello")
        self.exam_date_label.setStyleSheet("color: #333; font-size: 18px; font-weight: bold;")
        self.exam_date = QDateEdit()
        self.exam_date.setDisplayFormat("dd/MM/yyyy")
        self.exam_date.setFixedSize(300, 40)
        self.exam_date.setCalendarPopup(True)
        self.exam_date.setStyleSheet("""
            QDateEdit {
                background-color: #ffffff;
                color: #333;
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QDateEdit:focus {
                border: 1px solid #00796b;
            }
        """)

        self.load_exam_names()  # Carica la lista degli esami disponibili

        # Pulsante di inserimento
        self.add_button = QPushButton("Conferma")  # Testo del bottone
        self.add_button.setFixedSize(300, 40)  # Dimensioni
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #00796b;
                color: white;
                border-radius: 10px;
                font-size: 18px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #004d40;
            }
            QPushButton:pressed {
                background-color: #00251a;
            }
        """)  # Stile del bottone

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

        # Messaggio di conferma
        self.commit_message = QLabel("Appello aggiunto")  # Etichetta per il messaggio di errore
        self.commit_message.setFixedSize(300, 40)  # Dimensioni
        self.commit_message.setAlignment(Qt.AlignCenter)  # Allineamento al centro
        self.commit_message.setStyleSheet("color: green; font-size: 16px")  # Colore del testo
        self.commit_message.hide()  # Inizialmente nascosto

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Allineamento al centro di ogni widget
        self.layout.setSpacing(20)  # Spaziatura tra i widget

        # Aggiunta dei widget al layout
        self.layout.insertWidget(0, self.header_label)
        self.layout.addWidget(self.exam_name_label)
        self.layout.addWidget(self.exam_name)
        self.layout.addWidget(self.exam_course_label)
        self.layout.addWidget(self.exam_course)
        self.layout.addWidget(self.exam_date_label)
        self.layout.addWidget(self.exam_date)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.back_button)
        self.layout.addWidget(self.commit_message)
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

    def show_office_window(self): # Funzione per tornare alla pagina della segreteria
        self.close() # Chiude la pagina
        self.office_window.show() # Mostra la pagina della segreteria

    def load_exam_names(self): # Recupera l'elenco di esami disponibili dal database
        try:
            conn = connection() # Connessione al database
            cursor = conn.cursor() # Cursore per la query
            query = "SELECT DISTINCT NOMEESAME FROM ESAMI" # Query di selezione degli esami disponibili
            cursor.execute(query) # Esegue la query
            exams = cursor.fetchall()  # Recupera i risultati
            for exam in exams: # Aggiunge gli esami al QComboBox
                self.exam_name.addItem(exam[0])
            query = "SELECT DISTINCT NOMECORSO FROM CORSI" # Query di selezione dei corsi disponibili
            cursor.execute(query) # Esegue la query
            courses = cursor.fetchall() # Recupera i risultati
            for course in courses: # Aggiunge i corsi al QComboBox
                self.exam_course.addItem(course[0])
        except Error as e:
            print(f"Errore durante il caricamento dei nomi degli esami: {e}")
        finally:
            if conn.is_connected():
                cursor.close()  # Chiude il cursore
                conn.close()  # Chiude la connessione al database

    def add_exam(self): # Funzione per inserire un appello
        try:
            conn = connection()  # Connessione al database
            cursor = conn.cursor()  # Cursore per la query
            query = "INSERT INTO APPELLI (NOMEESAME, NOMECORSO, DATAESAME) VALUES (%s, %s, %s)"  # Query da eseguire
            data_esame = self.exam_date.date().toString("yyyy-MM-dd")
            cursor.execute(query, (self.exam_name.currentText(), self.exam_course.currentText(), data_esame))  # Esegue la query
            conn.commit() # Commit della query
            self.exam_name.setCurrentIndex(0) # Resetta l'indice del nome dell'esame
            self.exam_course.setCurrentIndex(0) # Resetta l'indice del nome del corso
            self.commit_message.show() # Mostra il messaggio di conferma
        except Error as e:
            print(f"Errore durante la connessione al database o inserimento dell'appello: {e}")
        finally:
            if conn.is_connected():
                cursor.close() # Chiude il cursore
                conn.close()  # Chiude la connessione al database