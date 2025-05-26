from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QComboBox, QHBoxLayout
from mysql.connector import Error

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

        # Matricola dello studente
        self.matricola_label = QLabel("Matricola")
        self.matricola_label.setStyleSheet("color: #333; font-size: 18px; font-weight: bold;")
        self.matricola = QLineEdit()
        self.matricola.setPlaceholderText("Matricola studente")
        self.matricola.setMaxLength(30)
        self.matricola.setFixedSize(300, 40)
        self.matricola.setStyleSheet("""
            QLineEdit {
                background-color: #f7f7f7;
                color: black;
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #00aaff;
                background-color: #ffffff;
            }
        """)

        # Voto dello studente
        self.grade_label = QLabel("Voto")
        self.grade_label.setStyleSheet("color: #333; font-size: 18px; font-weight: bold;")
        self.grade = QComboBox()
        for i in range(18, 31): # Range di voti possibili
            self.grade.addItem(str(i))
        self.grade.addItem("30 L") # Lode
        self.grade.setFixedSize(300, 40)
        self.grade.setStyleSheet("""
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
        self.exam_name_label = QLabel("Esame")
        self.exam_name_label.setStyleSheet("color: #333; font-size: 18px; font-weight: bold;")
        self.exam_name = QComboBox()
        self.exam_name.setFixedSize(300, 40)
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

        # Corso dell'esame
        self.exam_course_label = QLabel("Corso")
        self.exam_course_label.setStyleSheet("color: #333; font-size: 18px; font-weight: bold;")
        self.exam_course = QComboBox()
        self.exam_course.setFixedSize(300, 40)
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

        self.load_exam_names()  # Carica la lista degli esami disponibili

        # Pulsante per tornare alla home page
        self.back_button = QPushButton("Esci")
        self.back_button.setFixedSize(300, 40)
        self.back_button.clicked.connect(self.show_office_window)
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
        """)

        # Layout principale
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(20)

        # Layout per matricola e voto
        self.row1_layout = QHBoxLayout()
        self.row1_layout.setAlignment(Qt.AlignCenter)
        self.row1_layout.addWidget(self.matricola_label)
        self.row1_layout.addWidget(self.matricola)
        self.row1_layout.addWidget(self.grade_label)
        self.row1_layout.addWidget(self.grade)

        # Layout per nome esame e corso
        self.row2_layout = QHBoxLayout()
        self.row2_layout.setAlignment(Qt.AlignCenter)
        self.row2_layout.addWidget(self.exam_name_label)
        self.row2_layout.addWidget(self.exam_name)
        self.row2_layout.addWidget(self.exam_course_label)
        self.row2_layout.addWidget(self.exam_course)

        # Aggiunta widget al layout principale
        self.main_layout.addWidget(self.header_label)
        self.main_layout.addLayout(self.row1_layout)
        self.main_layout.addLayout(self.row2_layout)
        self.main_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        self.window = QWidget()
        self.window.setLayout(self.main_layout)
        self.setCentralWidget(self.window)

    def show_office_window(self):
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