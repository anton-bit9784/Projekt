import sqlite3
import hashlib # Um Passwörter zu sichern und nicht im Klasrtext speichern
from datetime import datetime, timedelta

# Verbindung zu SQLite-Datenbank
def get_db_connection():
    verbindung = sqlite3.connect("data/buchungen.db")
    verbindung.row_factory = sqlite3.Row  # Erlaubt Zugriff via Spaltennamen ohne Zahlen -> macht übersichtlicher
    return verbindung

# Hashing des Passwortes für die Sicherheit
def hash_passwort(passwort: str) -> str: 
    return hashlib.sha256(passwort.encode()).hexdigest()


# Erstellung der Tabellen für die Daten falls sie noch nicht existiert / Id immer +1
def init_db():
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()

    # 1. Tabelle für User
    zeiger.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        passwort_hash TEXT NOT NULL
    )
    """)

    # 2. Tabelle für Buchungsdaten
    zeiger.execute("""
    CREATE TABLE IF NOT EXISTS buchungssystem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        datum DATE NOT NULL,
        betrag REAL NOT NULL,
        name TEXT,
        kategorie TEXT NOT NULL,
        buchungstyp TEXT NOT NULL,
        beschreibung TEXT,
        FOREIGN KEY (username) REFERENCES users (username)
    )
    """)

    verbindung.commit()
    zeiger.close()
    verbindung.close()

def erstelle_benutzer(username, passwort):
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()
    try:
        zeiger.execute("""
        INSERT INTO users (username, passwort_hash)
        VALUES (?, ?)
        """, (username, hash_passwort(passwort)))

        verbindung.commit()
        erfolg = True # User erfolgreich erstellt
    except sqlite3.IntegrityError:
        erfolg = False # Username existiert bereits schon
    
    zeiger.close()
    verbindung.close()

    return erfolg

def ueberpruefe_benutzer(username, passwort):
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()
    zeiger.execute("""SELECT * FROM users WHERE username = ? AND passwort_hash = ?
    """, (username, hash_passwort(passwort)))
    user = zeiger.fetchone()
    zeiger.close()
    verbindung.close()

    return user is not None

# Speichert neue Buchung in Datenbank / ? Sind Platzhalter als Schutz
def speichere_buchung(buchung, username):
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()
    zeiger.execute("""
    INSERT INTO buchungssystem (username, datum, betrag, name, kategorie, buchungstyp, beschreibung)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, str(buchung.datum), buchung.betrag, buchung.name, buchung.kategorie, buchung.buchungstyp, buchung.beschreibung)) # Übermittlung an Datenbak
    
    verbindung.commit() # "Speichert" den Spaß
    zeiger.close()
    verbindung.close()

# Holt alle Buchungen vom user aus der Datenbank bzw. lädt die Daten zurück ins Frontend
def hole_alle_buchungen(username):
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()

    try:
        zeiger.execute("""SELECT * FROM buchungssystem WHERE username = ?
        """, [username]) # Zeiger Hollt alle Buchungen vom user
        reihen = zeiger.fetchall() # Wandelt SQL-Reihen in Python-Dicts um
        ergebnis = [dict(reihe) for reihe in reihen]
    except sqlite3.OperationalError: # Sicherheitznetz Falls Tabelle leer ist bzw. nicht existiert
        ergebnis = []  

    zeiger.close()
    verbindung.close()

    return ergebnis

# # Holt alle Buchungen welche zur Zeitspanne passen vom user aus der Datenbank bzw. lädt die Daten zurück ins Frontend
def hole_buchungen_bis_stichtag(stichtag_str: str, username: str):

    stichtag = datetime.strptime(stichtag_str, "%Y-%m-%d").date() 
    grenzdatum = stichtag - timedelta(days = 365)

    verbindung = get_db_connection()
    zeiger = verbindung.cursor()
    zeiger.execute("""SELECT * FROM buchungssystem WHERE username = ? AND datum >= ? AND datum <= ?
    """, (username, str(grenzdatum), str(stichtag)))

    reihen = zeiger.fetchall()
    ergebnis = [dict(reihe) for reihe in reihen]

    zeiger.close()
    verbindung.close()
    
    return ergebnis



# Zeiger = Typ der die Daten aus Datenbank nach Python macht 