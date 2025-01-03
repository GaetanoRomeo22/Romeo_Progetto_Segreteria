from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton

from Home import HomeWindow

class NextExamsPage(QMainWindow): # Finestra di visualizzazione degli appelli prenotati
    def __init__(self, next_exams):
        super().__init__()

        self.home_page = None # Finestra home page

        # Finestra
        self.setWindowTitle("Appelli prenotati")  # Titolo della finestra
        self.setFixedSize(800, 600)  # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica")  # Stile della finestra

        # Tabella
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nome Esame", "Corso", "Data Appello"])
        self.table.setRowCount(len(next_exams))  # Numero di righe basato sui dati

        # Popolamento della tabella
        for row_index, exam in enumerate(next_exams):
            for col_index, value in enumerate(exam):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

        self.table.setStyleSheet( # Stile della tabella
            """
            QTableWidget {
                border: 2px solid #cccccc;
                background-color: #ffffff;
                color: #333333;
                gridline-color: #cccccc;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                color: #333333;
                font-weight: bold;
                border: 1px solid #cccccc;
            }
            QTableWidget::item {
                border: 1px solid #cccccc;
            }
            """
        )
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Impedisce la modifica dei dati
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # Seleziona intere righe
        self.table.horizontalHeader().setStretchLastSection(True)  # La colonna finale riempie lo spazio
        self.table.verticalHeader().setVisible(False)  # Nasconde l'indice delle righe

        # Pulsante per tornare alla home page
        self.back_button = QPushButton("Home Page")
        self.back_button.setFixedSize(300, 40)  # Dimensioni
        self.back_button.setStyleSheet("background-color: green; color: white; border-radius: 5px; font-size: 18px")  # Stile del bottone
        self.back_button.clicked.connect(self.show_home_page)  # Funzione del bottone

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Allineamento al centro di ogni widget
        self.layout.setSpacing(20)  # Spaziatura tra i widget
        self.layout.addWidget(self.table)
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

    def show_home_page(self):
        self.close()  # Chiude la home page
        self.home_page = HomeWindow()  # Crea una finestra per visualizzare gli esami superati
        self.home_page.show()  # Mostra gli appelli prenotati