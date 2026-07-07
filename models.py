from pydantic import BaseModel
from datetime import date

# Definiert Datenstruktur der Buchungen
class BuchungStruktur(BaseModel):
    datum: date                
    betrag: float   
    name: str           
    kategorie: str             
    buchungstyp: str           
    beschreibung: str

# Definiert Datenstruktur für User
class UserStruktur(BaseModel):
    username: str
    passwort: str 