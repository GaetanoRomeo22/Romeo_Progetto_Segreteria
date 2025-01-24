from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel, \
    QHeaderView, QMessageBox
from datetime import datetime

from DatabaseConnection import connection

class NextExamsPage(QMainWindow): # Finestra di visualizzazione degli appelli prenotati
    def __init__(self, next_exams, home_page):
        super().__init__()

        self.home_page = home_page # Finestra home page

        # Finestra
        self.setWindowTitle("Appelli prenotati")  # Titolo della finestra
        # self.setFixedSize(800, 600)  # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica")  # Stile della finestra
        self.showFullScreen()  # Schermo intero

        # Intestazione
        self.header_label = QLabel("Appelli Prenotati")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00796b;
            margin-bottom: 20px;
            margin-top: 20px;
        """)

        # Tabella
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nome Esame", "Corso", "Data Appello", ""])
        self.table.setRowCount(len(next_exams))

        # Ridimensionamento uniforme delle colonne
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        # Popolamento della tabella
        for row_index, exam in enumerate(next_exams):
            for col_index, value in enumerate(exam):
                if col_index == 2:
                    value = datetime.strptime(value, "%Y-%m-%d").strftime("%d-%m-%Y") if isinstance(value,
                    str) else value.strftime("%d-%m-%Y")
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

        # Pulsante di annullamento di una prenotazione
        delete_button = QPushButton()
        delete_button.setIcon(QIcon("delete.jpeg"))  # Usa un'icona "X rossa"
        delete_button.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #ffe6e6;
            }
        """)
        delete_button.clicked.connect(lambda _, r=row_index: self.cancel_reservation(r))  # Collega la funzione
        self.table.setCellWidget(row_index, 3, delete_button)

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

    def cancel_reservation(self, row_index):  # Funzione per cancellare una prenotazione
        exam_name = self.table.item(row_index, 0).text()  # Nome dell'esame
        course_name = self.table.item(row_index, 1).text()  # Corso dell'esame

        # Messaggio di conferma
        confirmation = QMessageBox(self)
        confirmation.setWindowTitle("Conferma")
        confirmation.setIcon(QMessageBox.Question)
        confirmation.setText(f"<p style='font-size:16px; color:#333333;'>"
                             f"Vuoi davvero annullare la prenotazione per <b>'{exam_name}'</b> del corso <b>'{course_name}'</b>?"
                             f"</p>")
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
        response = confirmation.exec() # Mostra il messaggio e gestisci la risposta
        if response == QMessageBox.Yes:  # Se lo studente conferma
            try:
                conn = connection()  # Connessione al database
                cursor = conn.cursor()  # Cursore
                query = "DELETE FROM PRENOTA WHERE NOMEESAME = %s AND NOMECORSO = %s AND MATRICOLA = %s"  # Query di cancellazione della prenotazione
                cursor.execute(query, (exam_name, course_name, self.home_page.matricola))  # Esegue la query
                conn.commit()  # Conferma le modifiche
                self.table.removeRow(row_index)  # Rimuove la riga dalla tabella
                QMessageBox.information(self, "Successo", f"Prenotazione per '{exam_name}' annullata con successo!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore durante l'annullamento: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()  # Chiude il cursore
                    conn.close()  # Chiude la connessione al database