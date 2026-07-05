import streamlit as st
import requests
import pandas as pd
from datetime import date

# Aufbau der Website / Center 
st.set_page_config(page_title="Betriebliches Buchungssystem", layout="centered")

# Main Überschrift
st.title("💼 Betriebswirtschaftliches Buchungssystem")

st.markdown("---")

# Unter Überschrift
st.header("➕ Neue Buchung anlegen")

# Eingabefelt für neue Buchungen / Werden gelöscht nach Abgabe 
with st.form("buchungs_formular", clear_on_submit=True):
    eingabe_datum = st.date_input("Buchungsdatum", date.today())
    eingabe_betrag = st.number_input("Betrag (in €)", min_value=0.01, step=0.01, format="%.2f")
    eingabe_name = st.text_input("Name")
    eingabe_kategorie = st.text_input("Kategorie / Konto (z.B. Miete, Büromaterial)")
    eingabe_typ = st.selectbox("Buchungstyp", ["expense", "income"], format_func=lambda x: "Ausgabe" if x == "expense" else "Einnahme")
    eingabe_beschreibung = st.text_area("Beschreibung")
    
    abschicken = st.form_submit_button("Buchung speichern")

# Wenn abgeschickt wird erstellung eines Datenpackets (Buchung)
if abschicken:
    daten_paket = {
        "datum": str(eingabe_datum),
        "betrag": eingabe_betrag,
        "name": eingabe_name,
        "kategorie": eingabe_kategorie,
        "buchungstyp": eingabe_typ,
        "beschreibung": eingabe_beschreibung
    }
    
    try:
        antwort = requests.post("http://127.0.0.1:8000/buchung-erstellen", json=daten_paket) # Datenpacket (Buchung) wird versucht an Backend zu schicken
        if antwort.status_code == 200: # Wenn alles klappt bestätigungs Nachricht
            st.success("✅ Buchung erfolgreich über die API an die Datenbank übermittelt!")
        else: 
            st.error("❌ Fehler bei der Datenübertragung.") # Allgemienr Fehler Debugging
    except requests.exceptions.ConnectionError: # Fehler Backend läuft nicht -> Backend Starten
        st.error("❌ Das Backend läuft scheinbar nicht. Bitte starte zuerst backend.py!")

st.markdown("---")

# Unter Überschrift
st.header("📊 Auswertung & Buchungsübersicht")

try:
    antwort = requests.get("http://127.0.0.1:8000/buchungen") # Antowort wird vom Backend angfordert

    if antwort.status_code == 200:
        buchungs_liste = antwort.json() # buchungs_liste = Antwort aus dem Backend
        
        if buchungs_liste:
            df = pd.DataFrame(buchungs_liste) # Erstellung Tabelle 
            
            # Berechnung der Ergebnisse
            einnahmen = df[df["buchungstyp"] == "income"]["betrag"].sum() # Liste der Einnahmen
            ausgaben = df[df["buchungstyp"] == "expense"]["betrag"].sum() # Liste der Ausgaben
            gewinn_verlust = einnahmen - ausgaben 
            
            # Darstellung Ergebnisse in Diagramm 
            # Beschreibung der Columns / .metric damit Zahlen Fett
            col1, col2, col3 = st.columns(3)
            col1.metric("Gesamteinnahmen", f"{einnahmen:,.2f} €") 
            col2.metric("Gesamtausgaben", f"{ausgaben:,.2f} €")
            
            # Gewinn oder Verlust darstellen
            if gewinn_verlust >= 0: 
                col3.metric("Aktueller Gewinn", f"{gewinn_verlust:,.2f} €") 

            else:
                col3.metric("Aktueller Verlust", f"{gewinn_verlust:,.2f} €")
                
            chart_data = pd.DataFrame({
                "Betrag in €": [einnahmen, ausgaben],
                "Typ": ["Einnahmen", "Ausgaben"]
            }).set_index("Typ")
            
            st.bar_chart(chart_data) # Eigentlicher comand für Diagramm
            
            st.subheader("📋 Einzelbuchungen")

            ##st.write("Vorhandene Spalten:", df.columns.tolist()) # debugge Tool ignorrieren 
            vorhandene_spalten = [c for c in ["id", "betrag", "name", "kategorie", "buchungstyp", "beschreibung"] if c in df.columns] # Lowkey unnötig war wergen bug

            st.dataframe(df[vorhandene_spalten], width="stretch") # Darstellung alle Buchungen

        else:
            st.info("Noch keine Buchungen in der Datenbank vorhanden.") # Lehre Datenbank ._.

    else:
        st.error("Fehler beim Abrufen der Daten vom Backend.") # Fehler beim anfordern der Daten vom Backend

except requests.exceptions.ConnectionError:
    st.info("Warte auf Verbindung zum Backend...") # Fehler Backend läuft nicht -> Backend Starten