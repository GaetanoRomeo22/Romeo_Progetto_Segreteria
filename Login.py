from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMainWindow
from mysql.connector import Error

from Home import HomeWindow
from DatabaseConnection import connection


class LoginWindow(QMainWindow): # Finestra di login personalizzata
    def __init__(self):
        super().__init__()

        self.home_window = None # Finestra per la home page

        # Finestra
        self.setWindowTitle("Login") # Titolo della finestra
        self.setFixedSize(800, 600) # Dimensioni della finestra
        self.setStyleSheet("background-color: white;") # Stile della finestra

        # Logo
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter) # Allineamento al centro
        self.pixmap = QPixmap("uniparthenope.png") # Immagine logo
        self.pixmap = self.pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation) # Ridimensiona l'immagine
        self.logo.setPixmap(self.pixmap)

        # Username
        self.username_label = QLabel("Matricola") # Etichetta per l'username
        self.username_label.setStyleSheet("color: black; font-size: 16px") # Stile della casella di username
        # self.username_label.setAlignment(Qt.AlignCenter) # Allineamento al centro
        self.username = QLineEdit() # Casella di testo per l'username
        # username.setPlaceholderText("Matricola") # Placeholder
        self.username.setMaxLength(10) # Lunghezza massima del testo
        self.username.setFixedSize(300, 40) # Dimensioni della casella di testo
        self.username.setStyleSheet("background-color: #f7f7f7; color: black; font-size: 16px")

        # Password
        self.password_label = QLabel("Password") # Etichetta per la password
        self.password_label.setStyleSheet("color: black; font-size: 16px")  # Stile della casella di password
        # self.password_label.setAlignment(Qt.AlignCenter) # Allineamento al centro
        self.password = QLineEdit()  # Casella di testo per la password
        # self.password.setPlaceholderText("Password")  # Placeholder
        self.password.setMaxLength(30)  # Lunghezza massima del testo
        self.password.setEchoMode(QLineEdit.Password) # Nasconde la password
        self.password.setFixedSize(300, 40) # Dimensioni della casella di testo
        self.password.setStyleSheet("background-color: #f7f7f7; color: black; font-size: 16px")

        # Messaggio di errore
        self.error_message = QLabel("Accesso non riuscito") # Etichetta per il messaggio di errore
        self.error_message.setFixedSize(300, 40) # Dimensioni
        self.error_message.setAlignment(Qt.AlignCenter) # Allineamento al centro
        self.error_message.setStyleSheet("color: red; font-size: 16px") # Colore del testo
        self.error_message.hide() # Inizialmente nascosto

        # Pulsante di login
        self.login_button = QPushButton("Accedi") # Testo del bottone
        self.login_button.setFixedSize(300, 40) # Dimensioni
        self.login_button.setStyleSheet("background-color: green; color: white; border-radius: 5px; font-size: 18px") # Stile del bottone
        self.login_button.clicked.connect(self.handle_login) # Funzione del bottone

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter) # Allineamento al centro di ogni widget
        self.layout.setSpacing(20) # Spaziatura tra i widget
        self.layout.addWidget(self.logo)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.error_message)
        self.window = QWidget()
        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

    def handle_login(self): # Funzione di gestione del login
        if self.login(): # Se il login va a buon fine
            self.close()  # Chiude la finestra di login
            self.home_window = HomeWindow(self.username.text()) # Crea una finestra per la home page
            self.home_window.show() # Mostra la home page
        else: # Altrimenti
            self.error_message.show()  # Messaggio di errore

    def login(self) -> bool: # Funzione di login per lo studente
        try:
            conn = connection() # Connessione al database
            cursor = conn.cursor() # Cursore per la query
            query = "SELECT * FROM STUDENTI WHERE MATRICOLA = %s AND PASSWORD = %s" # Query da eseguire
            cursor.execute(query, (self.username.text(), self.password.text())) # Esegue la query
            result = cursor.fetchone() # Risultati della query
            if result: # Se è stato trovato un utente
                return True
            else: # Altrimenti
                return False
        except Error as e:
            print(f"Errore durante la connessione al database: {e}")
        finally:
            if conn.is_connected():
                conn.close()  # Chiude la connessione al database