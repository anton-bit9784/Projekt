from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
import sqlite3

app = FastAPI()

class BuchungStruktur(BaseModel):
    datum: date                
    betrag: float              
    kategorie: str             
    buchungstyp: str           
    beschreibung: str

@app.post("/buchung-erstellen")
def erstelle_buchung(neue_buchung: BuchungStruktur):
    verbindung = sqlite3.connect("datenbank.db")
    zeiger = verbindung.cursor()

    # Tabelle sicherheitshalber erstellen, falls sie noch nicht existiert
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
    verbindung = sqlite3.connect("datenbank.db")
    verbindung.row_factory = sqlite3.Row
    zeiger = verbindung.cursor()

    try:
        zeiger.execute("SELECT * FROM buchungssystem")
        reihen = zeiger.fetchall()
        ergebnis = [dict(reihe) for reihe in reihen]
    except sqlite3.OperationalError:
        ergebnis = [] # Falls Tabelle noch leer/nicht existent ist
        
    verbindung.close()
    return ergebnis

@app.get("/")
def home():
    return {"status": "Das SQ-Lite Backend läuft perfekt!"}