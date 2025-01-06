from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QFrame, QWidget

from AddExam import AddExamPage
from ValidateExam import ValidateExamPage


class OfficePage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.login_page = None # Pagina di login
        self.add_exam_page = None # Pagina di inserimento di un appello
        self.validate_exam_page = None # Pagina di convalida degli esami

        # Finestra
        self.setWindowTitle("Segreteria")  # Titolo della finestra
        # self.setFixedSize(800, 600)  # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica")  # Stile della finestra
        self.showFullScreen()  # Schermo intero

        # Intestazione
        self.header_label = QLabel("Segreteria")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            font-size: 24px;
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

        # Pulsante di inserimento di un appello
        self.adding_button = QPushButton("Inserimento Appelli")
        self.adding_button.setFixedSize(350, 50)  # Dimensioni
        self.adding_button.clicked.connect(self.show_add_exam_page)  # Funzione del bottone

        # Pulsante di convalida degli esami
        self.validate_button = QPushButton("Convalida Esami")
        self.validate_button.setFixedSize(350, 50)  # Dimensioni
        self.validate_button.clicked.connect(self.show_validate_exam_page)  # Funzione del bottone

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
        self.adding_button.setStyleSheet(button_style)
        self.validate_button.setStyleSheet(button_style)

        # Pulsante di logout
        self.logout_button = QPushButton("Logout")
        self.logout_button.setFixedSize(350, 50)  # Dimensioni
        self.logout_button.clicked.connect(self.logout)  # Funzione del bottone
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
                border: 2px solid #d32f2f;
            }
            QPushButton:pressed {
                background-color: #ff6659;
                border: 2px solid #b71c1c;
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
                padding: 30px;
                margin-top: 20px;
            }
        """)
        self.choices_layout = QVBoxLayout()
        self.choices_layout.setAlignment(Qt.AlignCenter)  # Allinea i pulsanti al centro
        self.choices_layout.setSpacing(25)  # Spaziatura tra i pulsanti

        # Aggiungere i pulsanti al layout
        self.choices_layout.addWidget(self.adding_button)
        self.choices_layout.addWidget(self.validate_button)
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

    def show_add_exam_page(self):
        self.close() # Chiude la pagina corrente
        self.add_exam_page = AddExamPage() # Crea una pagina per la creazione di un appello
        self.add_exam_page.show() # Mostra la pagina

    def show_validate_exam_page(self):
        self.close() # Chiude la pagina corrente
        self.validate_exam_page = ValidateExamPage() # Crea una pagina di validazione di un esame
        self.validate_exam_page.show() # Mostra la pagina

    def logout(self): # Funzione di logout per l'utente
        from Login import LoginWindow
        self.close() # Chiude la home page
        self.login_page = LoginWindow() # Crea una finestra di login
        self.login_page.show() # Mostra la finestra di login