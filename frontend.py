import streamlit as st
import requests
import pandas as pd
from datetime import date

st.set_page_config(page_title="Betriebliches Buchungssystem", layout="centered")

st.title("💼 Betriebswirtschaftliches Buchungssystem")
st.markdown("---")

st.header("➕ Neue Buchung anlegen")

with st.form("buchungs_formular", clear_on_submit=True):
    eingabe_datum = st.date_input("Buchungsdatum", date.today())
    eingabe_betrag = st.number_input("Betrag (in €)", min_value=0.01, step=0.01, format="%.2f")
    eingabe_kategorie = st.text_input("Kategorie / Konto (z.B. Miete, Büromaterial)")
    eingabe_typ = st.selectbox("Buchungstyp", ["expense", "income"], format_func=lambda x: "Ausgabe" if x == "expense" else "Einnahme")
    eingabe_beschreibung = st.text_area("Beschreibung")
    
    abschicken = st.form_submit_button("Buchung speichern")

if abschicken:
    daten_paket = {
        "datum": str(eingabe_datum),
        "betrag": eingabe_betrag,
        "kategorie": eingabe_kategorie,
        "buchungstyp": eingabe_typ,
        "beschreibung": eingabe_beschreibung
    }
    
    try:
        antwort = requests.post("http://127.0.0.1:8000/buchung-erstellen", json=daten_paket)
        if antwort.status_code == 200:
            st.success("✅ Buchung erfolgreich über die API an die Datenbank übermittelt!")
        else:
            st.error("❌ Fehler bei der Datenübertragung.")
    except requests.exceptions.ConnectionError:
        st.error("❌ Das Backend läuft scheinbar nicht. Bitte starte zuerst backend.py!")

st.markdown("---")

st.header("📊 Auswertung & Buchungsübersicht")

try:
    antwort = requests.get("http://127.0.0.1:8000/buchungen")
    if antwort.status_code == 200:
        buchungs_liste = antwort.json()
        
        if buchungs_liste:
            df = pd.DataFrame(buchungs_liste)
            
            einnahmen = df[df["buchungstyp"] == "income"]["betrag"].sum()
            ausgaben = df[df["buchungstyp"] == "expense"]["betrag"].sum()
            gewinn_verlust = einnahmen - ausgaben
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Gesamteinnahmen", f"{einnahmen:,.2f} €")
            col2.metric("Gesamtausgaben", f"{ausgaben:,.2f} €")
            
            if gewinn_verlust >= 0:
                col3.metric("Aktueller Gewinn", f"{gewinn_verlust:,.2f} €")
            else:
                col3.metric("Aktueller Verlust", f"{gewinn_verlust:,.2f} €")
                
            chart_data = pd.DataFrame({
                "Betrag in €": [einnahmen, ausgaben],
                "Typ": ["Einnahmen", "Ausgaben"]
            }).set_index("Typ")
            
            st.bar_chart(chart_data)
            
            st.subheader("📋 Einzelbuchungen")
            # Für neuere Streamlit-Versionen angepasst
            st.dataframe(df[["id", "datum", "betrag", "kategorie", "buchungstyp", "beschreibung"]], width=None)
        else:
            st.info("Noch keine Buchungen in der Datenbank vorhanden.")
    else:
        st.error("Fehler beim Abrufen der Daten vom Backend.")
except requests.exceptions.ConnectionError:
    st.info("Warte auf Verbindung zum Backend...")