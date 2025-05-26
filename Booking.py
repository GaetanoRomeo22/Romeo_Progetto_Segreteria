from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel, \
    QHeaderView, QMessageBox
from datetime import datetime
from mysql.connector import Error
from DatabaseConnection import connection


class BookingPage(QMainWindow): # Finestra di prenotazione degli appelli
    def __init__(self, matricola: str, home_page):
        super().__init__()

        self.home_page = home_page  # Finestra home page
        self.matricola = matricola
        self.available_exams = None

        # Finestra
        self.setWindowTitle("Prenotazione Appelli")  # Titolo della finestra
        # self.setFixedSize(800, 600)  # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica")  # Stile della finestra
        self.showFullScreen()  # Schermo intero

        # Intestazione
        self.header_label = QLabel("Appelli Disponibili")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00796b;
            margin-bottom: 20px;
            margin-top: 20px;
        """)

        self.book_exam() # Mostra gli appelli prenotabili

        # Tabella
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Esame", "Corso", "Data"])
        self.table.setRowCount(len(self.available_exams))

        # Ridimensionamento uniforme delle colonne
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Popolamento della tabella
        for row_index, exam in enumerate(self.available_exams):
            for col_index, value in enumerate(exam):
                if col_index == 2:
                    value = datetime.strptime(value, "%Y-%m-%d").strftime("%d-%m-%Y") if isinstance(value,
                            str) else value.strftime("%d-%m-%Y")
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

        # Stile tabella
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #cccccc;
                background-color: #ffffff;
                color: #333333;
                gridline-color: #cccccc;
                alternate-background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #00796b;
                color: white;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #cccccc;
            }
            QTableWidget::item {
                padding: 5px;
                border: 1px solid #cccccc;
            }
            QTableWidget::item:selected {
                background-color: #c8e6c9;
                color: #333333;
            }
        """)
        self.table.setAlternatingRowColors(True)  # Abilita i colori alternati
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Impedisce la modifica dei dati
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Seleziona intere righe
        self.table.verticalHeader().setVisible(False)  # Nasconde l'indice delle righe
        self.table.cellClicked.connect(self.confirm_booking)  # Collega la funzione di prenotazione al click della cella

        # Pulsante per tornare alla home page
        self.back_button = QPushButton("Esci")
        self.back_button.setFixedSize(300, 40)  # Dimensioni
        self.back_button.clicked.connect(self.show_home_page)  # Funzione del bottone
        self.back_button.setStyleSheet("""
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
                border: 2px solid #d32f2f;
            }
            QPushButton:pressed {
                background-color: #ff6659;
                border: 2px solid #b71c1c;
            }
        """)  # Stile del bottone

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Allineamento al centro di ogni widget
        self.layout.setSpacing(20)  # Spaziatura tra i widget

        # Aggiunta dei widget al layout
        self.layout.insertWidget(0, self.header_label)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

    def show_home_page(self):
        self.close()  # Chiude la pagina
        self.home_page.show()  # Mostra la home page

    def book_exam(self): # Funzione di prenotazione di un appello per lo studente
        try:
            conn = connection()  # Connessione al database
            cursor = conn.cursor()  # Cursore per la query
            query = "SELECT CORSOSTUDENTE FROM STUDENTI WHERE MATRICOLA = %s" # Query per estrapolare il corso dello studente
            cursor.execute(query, (self.matricola, )) # Esegue la query
            student_course = cursor.fetchone() # Salva il risultato
            query = ("""
                SELECT A.NOMEESAME, A.NOMECORSO, A.DATAESAME FROM APPELLI A WHERE A.NOMECORSO = %s AND A.DATAESAME > %s
                  AND A.NOMEESAME NOT IN (
                      SELECT P.NOMEESAME FROM PRENOTA P WHERE P.MATRICOLA = %s AND P.NOMECORSO = A.NOMECORSO)
            """) # Query per estrapolare gli appelli prenotabili
            current_date = datetime.now().date()  # Data corrente
            cursor.execute(query, (student_course[0], current_date, self.matricola))  # Esegue la query
            self.available_exams = cursor.fetchall()  # Risultati della query
        except Error as e:
            print(f"Errore durante la connessione al database: {e}")
        finally:
            if conn.is_connected():
                cursor.close()  # Chiude il cursore
                conn.close()  # Chiude la connessione al database

    def confirm_booking(self, row, column):
        exam_name = self.table.item(row, 0).text()
        course_name = self.table.item(row, 1).text()
        exam_date = self.table.item(row, 2).text()
        booking_date = datetime.now().date()

        confirmation = QMessageBox(self)
        confirmation.setWindowTitle("Prenotazione Appello")
        confirmation.setIcon(QMessageBox.Question)
        confirmation.setText(
            f"<p style='font-size:16px; color:#333333;'>"
            f"Confermi la prenotazione per:\n"
            f"Esame: {exam_name}\n"
            f"Corso: {course_name}\n"
            f"Data: {exam_date}?"
        )
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirmation.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
                color: #333333;
                font-family: Helvetica, Arial, sans-serif;
                font-size: 14px;
                border: 1px solid #cccccc;
            }
            QMessageBox QPushButton {
                background-color: #00796b;
                color: white;  # Imposta il colore del testo a bianco
                font-weight: bold;
                border: 1px solid #00796b;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
            QMessageBox QPushButton:hover {
                background-color: #005b4f;
            }
        """)
        reply = confirmation.exec_()  # Mostra il messaggio e gestisci la risposta

        if reply == QMessageBox.Yes:  # Se lo studente conferma
            try:
                conn = connection()
                cursor = conn.cursor()
                # Inserisci la prenotazione nel database
                query = "INSERT INTO PRENOTA (MATRICOLA, NOMEESAME, NOMECORSO, DATAPRENOTAZIONE) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (self.matricola, exam_name, course_name, booking_date))
                conn.commit()
                self.close()
                self.home_page.show()
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore durante la prenotazione: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()