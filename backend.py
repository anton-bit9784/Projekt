from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
import sqlite3
from models import BuchungStruktur
import utils

app = FastAPI()

# Erstellung der Tabelle für die Daten
utils.init_db()

# Speicher neue Buchungen in SQLite-Datenbank / Bestätigung wenn alles klapt 
@app.post("/buchung-erstellen")
def erstelle_buchung(neue_buchung: BuchungStruktur):
    utils.speichere_buchung(neue_buchung)
    return {"status": "Erfolgreich in der SQLite - Datenbank gespeichert!"}

# Abfrage der Liste mit allen gespeicherten Daten
@app.get("/buchungen")
def hole_buchungen():
    return utils.hole_alle_buchungen()

# Abfrage Liste der Buchungen zum Stichtag
@app.get("/buchungen/{stichtag}")
def hole_buchungen_stichtag(stichtag: str):
    return utils.hole_buchungen_bis_stichtag(stichtag)

# Home...
@app.get("/")
def home():
    return {"status": "Das SQ-Lite Backend läuft perfekt!"}