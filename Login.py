from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMainWindow, QHBoxLayout
from mysql.connector import Error

from Home import HomeWindow
from DatabaseConnection import connection
from Office import OfficePage


class LoginWindow(QMainWindow): # Finestra di login personalizzata
    def __init__(self):
        super().__init__()

        self.home_window = None # Finestra per la home page
        self.office_window = None # Finestra per la pagina della segreteria

        # Finestra
        self.setWindowTitle("Login") # Titolo della finestra
        # self.setFixedSize(800, 600) # Dimensioni della finestra
        self.setStyleSheet("background-color: white; font-family: Helvetica") # Stile della finestra
        self.showFullScreen() # Schermo intero

        # Intestazione
        self.header_label = QLabel("Login")
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #00796b;
            margin-bottom: 20px;
        """)

        # Logo
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter) # Allineamento al centro
        self.pixmap = QPixmap("logo.png") # Immagine logo
        self.pixmap = self.pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation) # Ridimensiona l'immagine
        self.logo.setPixmap(self.pixmap)
        self.logo.setStyleSheet("""
            margin-bottom: 20px;
            margin-top: 20px;
        """)

        # Username
        self.username_label = QLabel("Matricola") # Etichetta per l'username
        self.username_label.setStyleSheet("color: #333; font-size: 18px; font-weight: bold;") # Stile della casella di username
        # self.username_label.setAlignment(Qt.AlignCenter) # Allineamento al centro
        self.username = QLineEdit() # Casella di testo per l'username
        self.username.setPlaceholderText("Inserisci la tua matricola") # Placeholder
        self.username.setMaxLength(10) # Lunghezza massima del testo
        self.username.setFixedSize(300, 40) # Dimensioni della casella di testo
        self.username.setStyleSheet("""
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

        # Password
        self.password_label = QLabel("Password") # Etichetta per la password
        self.password_label.setStyleSheet("color: #333; font-size: 18px; font-weight: bold;")  # Stile della casella di password
        # self.password_label.setAlignment(Qt.AlignCenter) # Allineamento al centro
        self.password = QLineEdit()  # Casella di testo per la password
        self.password.setPlaceholderText("Inserisci la tua password")  # Placeholder
        self.password.setMaxLength(30)  # Lunghezza massima del testo
        self.password.setEchoMode(QLineEdit.Password) # Nasconde la password
        self.password.setFixedSize(300, 40) # Dimensioni della casella di testo
        self.password.setStyleSheet("""
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

        # Pulsante mostra/nascondi password
        self.toggle_password_button = QPushButton("👁")
        self.toggle_password_button.setFixedSize(40, self.password.height())
        self.toggle_password_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                font-size: 16px;
                color: #555;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                color: #00796b;
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: #e0e0e0;
            }
        """)
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)

        # Layout orizzontale per password e pulsante
        self.password_layout = QHBoxLayout()
        self.password_layout.addWidget(self.password)
        self.password_layout.addWidget(self.toggle_password_button)
        self.password_layout.setSpacing(10)

        # Messaggio di errore
        self.error_message = QLabel("Accesso non riuscito") # Etichetta per il messaggio di errore
        self.error_message.setFixedSize(300, 40) # Dimensioni
        self.error_message.setAlignment(Qt.AlignCenter) # Allineamento al centro
        self.error_message.setStyleSheet("color: red; font-size: 16px") # Colore del testo
        self.error_message.hide() # Inizialmente nascosto

        # Pulsante di login
        self.login_button = QPushButton("Accedi") # Testo del bottone
        self.login_button.setFixedSize(300, 40) # Dimensioni
        self.login_button.setStyleSheet("""
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
        """) # Stile del bottone
        self.login_button.clicked.connect(self.login) # Funzione del bottone

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter) # Allineamento al centro di ogni widget
        self.layout.setSpacing(20) # Spaziatura tra i widget

        # Aggiunta dei widget al layout
        self.layout.insertWidget(0, self.header_label)
        self.layout.addWidget(self.logo)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.password_label)
        self.layout.addLayout(self.password_layout)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.error_message)
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

    def login(self): # Funzione di login per lo studente
        if self.username.text() == self.password.text() == "admin": # Se l'utente è della segreteria
            self.office_window = OfficePage()  # Crea una finestra per la segreteria
            self.office_window.show()  # Mostra la pagina della segreteria
        else: # Altrimenti
            try:
                conn = connection() # Connessione al database
                cursor = conn.cursor() # Cursore per la query
                query = "SELECT * FROM STUDENTI WHERE MATRICOLA = %s AND PASSWORD = %s" # Query da eseguire
                cursor.execute(query, (self.username.text(), self.password.text())) # Esegue la query
                result = cursor.fetchone() # Risultati della query
                if result: # Se è stato trovato un utente
                    self.close()  # Chiude la finestra di login
                    self.home_window = HomeWindow(self.username.text(), result[3] + " " + result[4])  # Crea una finestra per la home page
                    self.home_window.show()  # Mostra la home page
                else: # Altrimenti
                    self.error_message.show()  # Messaggio di errore
            except Error as e:
                print(f"Errore durante la connessione al database: {e}")
            finally:
                if conn.is_connected():
                    cursor.close()  # Chiude il cursore
                    conn.close()  # Chiude la connessione al database

    def toggle_password_visibility(self): # Funzione per mostrare/nascondere la password
        if self.password.echoMode() == QLineEdit.Password:
            self.password.setEchoMode(QLineEdit.Normal)
            self.toggle_password_button.setText("🔒")
        else:
            self.password.setEchoMode(QLineEdit.Password)
            self.toggle_password_button.setText("👁")
