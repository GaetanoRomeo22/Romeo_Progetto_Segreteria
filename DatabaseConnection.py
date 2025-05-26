import mysql.connector


def connection() -> 'mysql.connector.connection.MySQLConnection | None': # Funzione di connessione al database
    """
    Tenta di connettersi al database MySQL.
    Ritorna la connessione se va a buon fine, altrimenti None.
    """
    try:
        conn = mysql.connector.connect( # connessione al database
            host="localhost",
            user="root",
            password="Gaetano22",
            database="Segreteria",
            connection_timeout=5
        )
        if conn.is_connected(): # Se la connessione è andata a buon fine
            print("Connessione al database MySQL avvenuta con successo!")
            return conn
        else:
            print("Connessione al database MySQL fallita!")
            return None
    except Exception as exp:
        print(f"Errore durante la connessione al database: {exp}")
        return None