from fastapi import FastAPI, HTTPException # An HTTP exception you can raise in your own code to show errors to the client. This is for client errors, invalid authentication, invalid data, etc. Not for server errors in your code.
from pydantic import BaseModel
from datetime import date
import sqlite3
from models import BuchungStruktur, UserStruktur
import utils

app = FastAPI()

# Erstellung der Tabelle für die Daten
utils.init_db()

# Registierung des Benutzers / checken ob Username schon existiert
@app.post("/registrierung")
def registrierung(user: UserStruktur):
    erfolg = utils.erstelle_benutzer(user.username, user.passwort)
    if not erfolg:
        raise HTTPException(status_code = 400, detail = "Benutzername bereits vergeben.")
    return {"status": "Registrierung erfolgreich"}

# Login des Benutzers checken ob User auch "Account" hat
@app.post("/login")
def login(user: UserStruktur):
    gueltig = utils.ueberpruefe_benutzer(user.username, user.passwort)
    if not gueltig: 
        raise HTTPException(status_code = 401, detail = "Falscher Benutzername oder Passwort.")
    return {"status": "Login erfolgreich!"}

# Speicher neue Buchungen in Datenbank / Bestätigung wenn alles klapt 
@app.post("/buchung-erstellen")
def erstelle_buchung(neue_buchung: BuchungStruktur, username: str):
    utils.speichere_buchung(neue_buchung, username)
    return {"status": "Erfolgreich in der SQLite - Datenbank gespeichert!"}

# Abfrage der Liste mit allen gespeicherten Daten
@app.get("/buchungen")
def hole_buchungen(username: str):
    return utils.hole_alle_buchungen(username)

# Abfrage Liste der Buchungen zum Stichtag
@app.get("/buchungen/stichtag/{stichtag}")
def hole_buchungen_stichtag(stichtag: str, username: str):
    return utils.hole_buchungen_bis_stichtag(stichtag, username)

# Home...
@app.get("/")
def home():
    return {"status": "Das SQ-Lite Backend läuft perfekt!"}