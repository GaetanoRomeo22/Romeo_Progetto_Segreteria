from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel, \
    QHeaderView, QAbstractItemView
from mysql.connector import Error

from DatabaseConnection import connection


class CareerPage(QMainWindow): # Finestra per la visualizzazione del libretto dello studente
    def __init__(self, matricola: str, home_page):
        super().__init__()

        self.home_page = home_page  # Finestra home page
        self.matricola = matricola
        self.given_exams = None

        # Finestra
        self.setWindowTitle("Libretto")  # Titolo della finestra
        # self.setFixedSize(800, 600)  # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica")  # Stile della finestra
        self.showFullScreen()  # Schermo intero

        # Intestazione
        self.header_label = QLabel("Esami Sostenuti")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00796b;
            margin-bottom: 20px;
            margin-top: 20px;
        """)

        self.show_given_exams() # Mostra gli esami superati

        # Tabella
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Esame", "Corso", "Voto", "Data"])
        self.table.setRowCount(len(self.given_exams))

        # Ridimensionamento uniforme delle colonne
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Popolamento della tabella
        for row_index, exam in enumerate(self.given_exams):
            for col_index, value in enumerate(exam):
                if col_index == 3:
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
        self.table.setAlternatingRowColors(True) # Abilita i colori alternati
        self.table.setEditTriggers(QTableWidget.NoEditTriggers) # Impedisce la modifica dei dati
        self.table.setSelectionMode(QAbstractItemView.NoSelection) # Disabilita la selezione
        self.table.verticalHeader().setVisible(False) # Nasconde l'indice delle righe

        # Pulsante per tornare alla home page
        self.back_button = QPushButton("Esci")
        self.back_button.setFixedSize(300, 40) # Dimensioni
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
        self.layout.setAlignment(Qt.AlignCenter) # Allineamento al centro di ogni widget
        self.layout.setSpacing(20) # Spaziatura tra i widget

        # Aggiunta dei widget al layout
        self.layout.insertWidget(0, self.header_label)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

    def show_home_page(self):
        self.close() # Chiude la pagina
        self.home_page.show() # Mostra la home page

    def show_given_exams(self): # Funzione di visualizzazione degli esami dati dallo studente
        try:
            conn = connection() # Connessione al database
            cursor = conn.cursor()  # Cursore per la query
            query = ("SELECT A.NOMEESAME, A.NOMECORSO, SP.VOTO, A.DATAESAME FROM SUPERA SP "
                     " JOIN APPELLI A ON SP.NOMEESAME = A.NOMEESAME AND SP.NOMECORSO = A.NOMECORSO"
                     " AND A.DATAESAME <= CURRENT_DATE WHERE SP.MATRICOLA = %s")  # Query da eseguire
            cursor.execute(query, (self.matricola, )) # Esegue la query
            self.given_exams = cursor.fetchall()  # Risultati della query
        except Error as e:
            print(f"Errore durante la connessione al database: {e}")
        finally:
            if conn.is_connected():
                cursor.close()  # Chiude il cursore
                conn.close()  # Chiude la connessione al database