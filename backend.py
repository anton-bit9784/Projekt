from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
import sqlite3
from models import BuchungStruktur
import utils

app = FastAPI()

utils.init_db()

@app.post("/buchung-erstellen")
def erstelle_buchung(neue_buchung: BuchungStruktur):
    utils.speichere_buchung(neue_buchung)
    return {"status": "Erfolgreich in der SQLite - Datenbank gespeichert!"}
    
@app.get("/buchungen")
def hole_buchungen():
    return utils.hole_alle_buchungen()

@app.get("/")
def home():
    return {"status": "Das SQ-Lite Backend läuft perfekt!"}