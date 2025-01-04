from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel, \
    QHeaderView
from datetime import datetime


class BookingPage(QMainWindow): # Finestra di prenotazione degli appelli
    def __init__(self, available_exams, home_page):
        super().__init__()

        self.home_page = home_page  # Finestra home page

        # Finestra
        self.setWindowTitle("Prenotazione Appelli")  # Titolo della finestra
        # self.setFixedSize(800, 600)  # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica")  # Stile della finestra
        self.showFullScreen()  # Schermo intero

        # Intestazione
        self.header_label = QLabel("Appelli Disponibili")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #00796b;
            margin-bottom: 10px;
        """)

        # Tabella
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nome Esame", "Corso", "Data Appello"])
        self.table.setRowCount(len(available_exams))

        # Ridimensionamento uniforme delle colonne
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Popolamento della tabella
        for row_index, exam in enumerate(available_exams):
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

        # Pulsante per tornare alla home page
        self.back_button = QPushButton("Home Page")
        self.back_button.setFixedSize(300, 40)  # Dimensioni
        self.back_button.setStyleSheet("""
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
        """)  # Stile del bottone
        self.back_button.clicked.connect(self.show_home_page)  # Funzione del bottone

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