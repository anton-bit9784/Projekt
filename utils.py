import sqlite3

# 1. Verbindung zu SQLite-Datenbank
def get_db_connection():
    """Erstellt eine saubere Verbindung zur SQLite-Datenbank."""
    verbindung = sqlite3.connect("data/buchungen.db")
    verbindung.row_factory = sqlite3.Row  # Erlaubt Zugriff via Spaltennamen
    return verbindung

def init_db():
    """Erstellt die Tabelle, falls sie noch nicht existiert."""
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()
    zeiger.execute("""
    CREATE TABLE IF NOT EXISTS buchungssystem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datum TEXT NOT NULL,
        betrag REAL NOT NULL,
        name TEXT,
        kategorie TEXT NOT NULL,
        buchungstyp TEXT NOT NULL,
        beschreibung TEXT
    )
    """)
    verbindung.commit()
    verbindung.close()

def speichere_buchung(buchung):
    """Speichert eine neue Buchung in der Datenbank."""
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()
    zeiger.execute("""
    INSERT INTO buchungssystem (datum, betrag, name, kategorie, buchungstyp, beschreibung)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (str(buchung.datum), buchung.betrag, buchung.name, buchung.kategorie, buchung.buchungstyp, buchung.beschreibung))
    verbindung.commit()
    verbindung.close()

def hole_alle_buchungen():
    """Holt alle Buchungen aus der Datenbank."""
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()
    try:
        zeiger.execute("SELECT * FROM buchungssystem")
        reihen = zeiger.fetchall() # Wandelt SQL-Reihen in Python-Dicts um
        ergebnis = [dict(reihe) for reihe in reihen]
    except sqlite3.OperationalError:
        ergebnis = [] # Falls Tabelle noch leer/nicht existent ist
    verbindung.close()
    return ergebnis