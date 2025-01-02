import sys
from PyQt5.QtWidgets import QApplication
from Login import LoginWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Unica istanza di QApplication per il progetto
    window = LoginWindow()  # Nuova finestra
    window.show()  # Mostra la finestra
    app.exec()  # Avvia l'esecuzione