from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
import sqlite3

app = FastAPI()

# 1. Definiert Datenstruktur
class BuchungStruktur(BaseModel):
    datum: date                
    betrag: float              
    kategorie: str             
    buchungstyp: str           
    beschreibung: str

# 2. VErbindung zu SQLite-Datenbank
def get_db_connection():
    """Erstellt eine saubere Verbindung zur SQLite-Datenbank."""
    verbindung = sqlite3.connect("datenbank.db")
    verbindung.row_factory = sqlite3.Row  # Erlaubt Zugriff via Spaltennamen
    return verbindung


@app.post("/buchung-erstellen")
def erstelle_buchung(neue_buchung: BuchungStruktur):
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()

    # Tabelle erstellen, falls nicht vorhanden
    zeiger.execute("""
    CREATE TABLE IF NOT EXISTS buchungssystem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datum TEXT NOT NULL,
        betrag REAL NOT NULL,
        kategorie TEXT NOT NULL,
        buchungstyp TEXT NOT NULL,
        beschreibung TEXT
    )
    """)

    # Daten sicher einfuegen 
    zeiger.execute(""" 
    INSERT INTO buchungssystem (datum, betrag, kategorie, buchungstyp, beschreibung) 
    VALUES (?, ?, ?, ?, ?)
    """, (
        str(neue_buchung.datum), 
        neue_buchung.betrag,
        neue_buchung.kategorie,
        neue_buchung.buchungstyp,
        neue_buchung.beschreibung
    ))
    verbindung.commit()
    verbindung.close()

    return {"status": "Erfolgreich in der SQLite - Datenbank gespeichert!"}
    
@app.get("/buchungen")
def hole_alle_buchungen():
    verbindung = get_db_connection()
    zeiger = verbindung.cursor()

    try:
        zeiger.execute("SELECT * FROM buchungssystem")
        reihen = zeiger.fetchall()
        # Wandelt SQL-Reihen in Python-Dicts um
        ergebnis = [dict(reihe) for reihe in reihen]
    except sqlite3.OperationalError:
        ergebnis = [] # Falls Tabelle noch leer/nicht existent ist
        
    verbindung.close()
    return ergebnis

@app.get("/")
def home():
    return {"status": "Das SQ-Lite Backend läuft perfekt!"}