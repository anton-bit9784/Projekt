from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
import sqlite3

# Definiert Datenstruktur der Buchungen
class BuchungStruktur(BaseModel):
    datum: date                
    betrag: float   
    name: str           
    kategorie: str             
    buchungstyp: str           
    beschreibung: str