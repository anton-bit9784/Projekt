import sqlite3

# Verbindung zu SQLite-Datenbank
def get_db_connection():
    verbindung = sqlite3.connect("data/buchungen.db")
    verbindung.row_factory = sqlite3.Row  # Erlaubt Zugriff via Spaltennamen ohne Zahlen -> macht übersichtlicher
    return verbindung

# Erstellung der Tabelle für die Daten falls sie noch nicht existiert / Id immer +1
def init_db():
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()
    zeiger.execute("""
    CREATE TABLE IF NOT EXISTS buchungssystem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datum DATE NOT NULL,
        betrag REAL NOT NULL,
        name TEXT,
        kategorie TEXT NOT NULL,
        buchungstyp TEXT NOT NULL,
        beschreibung TEXT
    )
    """)

    verbindung.commit()
    zeiger.close()
    verbindung.close()

# Speichert neue Buchung in Datenbank / ? Sind Platzhalter als Schutz
def speichere_buchung(buchung):
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()
    zeiger.execute("""
    INSERT INTO buchungssystem (datum, betrag, name, kategorie, buchungstyp, beschreibung)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (str(buchung.datum), buchung.betrag, buchung.name, buchung.kategorie, buchung.buchungstyp, buchung.beschreibung)) # Übermittlung an Datenbak
    
    verbindung.commit() # "Speichert" den Spaß
    zeiger.close()
    verbindung.close()

# Holt alle Buchungen aus der Datenbank bzw. lädt die Daten zurück ins Frontend
def hole_alle_buchungen():
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()

    try:
        zeiger.execute("SELECT * FROM buchungssystem") # Zeiger Hollt alle Buchungen
        reihen = zeiger.fetchall() # Wandelt SQL-Reihen in Python-Dicts um
        ergebnis = [dict(reihe) for reihe in reihen]
    except sqlite3.OperationalError: # Sicherheitznetz Falls Tabelle leer ist bzw. nicht existiert
        ergebnis = [] 

    zeiger.close()
    verbindung.close()

    return ergebnis

def hole_buchungen_bis_stichtag(stichtag: str):
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()
    zeiger.execute("SELECT * FROM buchungssystem WHERE datum <= ?", (stichtag,))
    reihen = zeiger.fetchall()
    ergebnis = [dict(reihe) for reihe in reihen]

    zeiger.close()
    verbindung.close()
    return ergebnis



# Zeiger = Typ der die Daten aus Datenbank nach Python macht 