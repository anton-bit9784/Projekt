import streamlit as st
import requests
import pandas as pd
from datetime import date, timedelta 

# Aufbau der Website / Center 
st.set_page_config(page_title="Betriebliches Buchungssystem", layout="centered")

BACKEND_URL = "http://127.0.0.1:8000" 

# Session State Variablen erstellen falls nicht vorhanden
if "eingeloggt" not in st.session_state:
    st.session_state["eingeloggt"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

# LOGIN UND REGISTIERUNGS INTERFACE 

if not st.session_state["eingeloggt"]:
    st.title("🔐 Login / Registierung")

    tab1, tab2 = st.tabs(["Anmelden", "Konto erstellen"])

    with tab1:
        st.subheader("Login")
        login_user = st.text_input("Benutzername", key = "login_user")
        login_passwort = st.text_input("Passwort", type = "password", key = "login_passwort")

        if st.button("Einloggen"): 
            try:
                antwort = requests.post(f"{BACKEND_URL}/login", json={"username": login_user, "passwort": login_passwort}) 
                if antwort.status_code == 200:
                    st.session_state["eingeloggt"] = True 
                    st.session_state["username"] = login_user
                    st.rerun() # Lädt Seite neu um Dashbloard anzuzeigen
                else:
                    st.error("❌ " + antwort.json().get("detail", "Login fehlgeschlagen."))
            except requests.exceptions.ConnectionError:
                st.error("❌ Das Backend läuft scheinbar nicht. Bitte starte zuerst backend.py!")

    with tab2:
        st.subheader("Registrierung")
        reg_user = st.text_input("Benutzername", key = "reg_user")
        reg_passwort = st.text_input("Passwort", type = "password", key = "reg_passwort")

        if st.button("Konto erstellen"):
            if reg_user and reg_passwort:
                try:
                    antwort = requests.post(f"{BACKEND_URL}/registrierung", json = {"username": reg_user, "passwort": reg_passwort})
                    if antwort.status_code == 200:
                        st.success("🎉 Konto erfolgreich erstellt! Du kannst dich jetzt anmelden.")
                    else:
                        st.error("❌ " + antwort.json().get("detail", "Fehler."))
                except requests.exceptions.ConnectionError:
                    st.error("❌ Das Backend läuft scheinbar nicht. Bitte starte zuerst backend.py!")
            else: 
                st.warning("Bitte fülle alle Felder aus.")

# BUCHUNGSSYSTEM

else: 
    current_user = st.session_state["username"]

    # Sidebar für Logout und User-Info
    st.sidebar.title(f"👤 Hallo, {current_user}!")
    if st.sidebar.button("Abmelden"):
        st.session_state["eingeloggt"] = False
        st.session_state["username"] = ""
        st.rerun() 

    st.title("💼 Betriebswirtschaftliches Buchungssystem")
    st.markdown("---")

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
            antwort = requests.post(f"{BACKEND_URL}/buchung-erstellen?username={current_user}", json=daten_paket) # Datenpacket (Buchung) wird versucht an Backend zu schicken / Username als Query-Parameter angehängt
        
            if antwort.status_code == 200: # Wenn alles klappt bestätigungs Nachricht
                st.success("✅ Buchung erfolgreich über die API an die Datenbank übermittelt!")

            else: 
                st.error("❌ Fehler bei der Datenübertragung.") # Allgemienr Fehler
    
        except requests.exceptions.ConnectionError: # Fehler Backend läuft nicht -> Backend Starten
            st.error("❌ Das Backend läuft scheinbar nicht. Bitte starte zuerst backend.py!")

    st.markdown("---")

    st.header("📅 Bilanz zu einem Stichtag")

    heute = date.today()
    ein_jahr_zurueck = heute - timedelta(days=365)

    stichtag = st.date_input(
        "Wähle einen Stichtag (max. 1 Jahr zurück)", 
        value = heute,
        min_value = ein_jahr_zurueck,
        max_value = heute
    )

    if st.button("Bilanz berechnen"):
        antwort = requests.get(f"{BACKEND_URL}/buchungen/stichtag/{stichtag}?username={current_user}")

        if antwort.status_code == 200:
            bilanz_liste = antwort.json()

            if bilanz_liste:
                df_stichtag = pd.DataFrame(bilanz_liste)
                einnahmen_stichtag = df_stichtag[df_stichtag["buchungstyp"] == "income"]["betrag"].sum()
                ausgaben_stichtag = df_stichtag[df_stichtag["buchungstyp"] == "expense"]["betrag"].sum()

                st.write(f"### Bilanz zum {stichtag}")
                st.metric("Summe Einnahmen", f"{einnahmen_stichtag:,.2f} €")
                st.metric("Summe Ausgaben", f"{ausgaben_stichtag:,.2f} €")
                st.metric("Saldo", f"{(einnahmen_stichtag - ausgaben_stichtag):,.2f} €")
            else:
                st.info("Keine Buchungen im Zeitraum der letzten 12 Monate bis zum gewählten Stichtag gefunden.")

        else:
            st.error("Fehler beim Abrufen der Daten vom Backend.") # Fehler beim anfordern der Daten vom Backend


    st.markdown("---")

    # Unter Überschrift
    st.header("📊 Auswertung & Buchungsübersicht")

    try:
        antwort = requests.get(f"{BACKEND_URL}/buchungen?username={current_user}") # Antowort wird vom Backend angfordert

        if antwort.status_code == 200:
            buchungs_liste = antwort.json() # buchungs_liste = Antwort aus dem Backend
        
            if buchungs_liste:
                df = pd.DataFrame(buchungs_liste) # Erstellung Tabelle / Umwandlung in Pandas-Format
            
                # Berechnung der Ergebnisse
                einnahmen = df[df["buchungstyp"] == "income"]["betrag"].sum() # Liste der Einnahmen
                ausgaben = df[df["buchungstyp"] == "expense"]["betrag"].sum() # Liste der Ausgaben
                gewinn_verlust = einnahmen - ausgaben 
            
                # Darstellung Ergebnisse in Diagramm 
                # Beschreibung der Columns / .metric damit Zahlen Fett
                col1, col2, col3 = st.columns(3)
                col1.metric("Gesamteinnahmen", f"{einnahmen:,.2f} €") 
                col2.metric("Gesamtausgaben", f"{ausgaben:,.2f} €")
            
                # col3 / Gewinn oder Verlust darstellen
                if gewinn_verlust >= 0: 
                    col3.metric("Aktueller Gewinn", f"{gewinn_verlust:,.2f} €") 
                else:
                    col3.metric("Aktueller Verlust", f"{gewinn_verlust:,.2f} €")
                
                chart_data = pd.DataFrame({ # Sieht man wenn über Balken rüber geht
                    "Betrag in €": [einnahmen, ausgaben],
                    "Typ": ["Einnahmen", "Ausgaben"]
                }).set_index("Typ")
            
                st.bar_chart(chart_data) # Eigentlicher comand für Diagramm
            
                st.subheader("📋 Einzelbuchungen")

                ##st.write("Vorhandene Spalten:", df.columns.tolist()) # debugge Tool ignorrieren 
                vorhandene_spalten = [c for c in ["id", "datum", "betrag", "name", "kategorie", "buchungstyp", "beschreibung"] if c in df.columns] # Lowkey unnötig war wergen bug
                st.dataframe(df[vorhandene_spalten], width="stretch") # Darstellung alle Buchungen

            else:
                st.info("Noch keine Buchungen in der Datenbank vorhanden.") # Lehre Datenbank ._.

        else:
            st.error("Fehler beim Abrufen der Daten vom Backend.") # Fehler beim anfordern der Daten vom Backend

    except requests.exceptions.ConnectionError:
        st.info("Warte auf Verbindung zum Backend...") # Fehler Backend läuft nicht -> Backend Starten