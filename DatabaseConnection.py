import mysql.connector
from mysql.connector import Error


def connection(): # Funzione di connessione al database
    try:
        conn = mysql.connector.connect( # connessione al database
            host="localhost",
            user="root",
            password="Gaetano22",
            database="Segreteria"
        )
        if conn.is_connected(): # Se la connessione è andata a buon fine
            print("Connessione al database MySQL avvenuta con successo!")
        else:
            print("Connessione al database MySQL fallita!")
        return conn
    except Error as e:
        print(f"Errore durante la connessione al database: {e}")
        return None