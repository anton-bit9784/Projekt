# Projekt

Gruppenmitglieder: 

Alexander Bauer
Anton Geibel

Projektbeschreibung: 

Bei dieser Anwendung handelt es sich um ein betriebswirtschaftliches Buchungssystem, welches Buchungen aufnehmen und in einer lokalen Datenbank speichern kann. Darüber hinaus ermöglicht das System eine detaillierte Auswertung mittels einer Bilanz, die zu einem frei wählbaren Stichtag berechnet wird, sowie eine grafische Visualisierung der Einnahmen und Ausgaben. Zudem besitzt das System als kreative Erweiterung ein interaktives User-Interface. 

Aufbau des Projekts:

Das Projekt ist in vier Python-Dateien aufgeteilt: 
- frontend.py: Steuert die Benutzeroberfläche und die grafischen Darstellungen in Streamlit.
- backend.py: Bereitstellt die API-Endpunkte über FastAPI, um Anfragen vom Frontend zu verarbeiten.
- utils.py: Enthält die Hintergrundlogik und die direkten Datenbank-Werkzeuge (z. B. das Erstellen von Tabellen, das Speichern, Laden und Filtern von Daten).
- models.py: Definiert die exakte Datenstruktur (Daten-Baupläne) für die Validierung der Objekte.

Beschreibung der kreativen Erweiterung: 

Als kreative Erweiterung wurde ein User-Interface zur Benutzerverwaltung integriert. Hierüber können sich Nutzer registrieren oder mit einem bestehenden Account anmelden. Sobald ein Benutzer eingeloggt ist, kann er ausschließlich seine eigenen Buchungen einsehen. Außerdem werden die Passwörter niemals im Klartext, sondern als sicherer SHA-256-Hash in der Datenbank gespeichert. 
Vorhandene Test-Accounts: 
Benutzername            Passwort
    Anton                 1234
    Alex                  123

Starten der Anwendung:

Um die Anwendung zu starten, sollte man zwei separate Instanzen in der Konsole öffnen, sich zum Projektordner bewegen und jeweils die virtuelle Umgebung mit folgendem Kommando ".venv\Scripts\activate" aktivieren. Anschließend in der ersten Konsolen-Instanz das Backend starten mit "uv run uvicorn backend:app --reload". Und in der zweiten Konsolen-Instanz das Frontend mit "uv run streamlit run frontend.py". Nach dem Start öffnet sich die Webanwendung automatisch im Browser und zeigt die Login-Seite an. Dort kann man sich mit den Test-Accounts anmelden oder ein neues Konto erstellen.

Nutzung von KI:

Wir haben prinzipiell immer versucht, unsere Vorhaben zunächst komplett ohne KI zu programmieren. Da wir beide jedoch noch keine nennenswerte Programmiererfahrung besitzen, sind wir regelmäßig auf Hürden gestoßen. Wenn wir Probleme selbstständig nicht beheben konnten, haben wir das KI-Tool Gemini als Unterstützung genutzt.

Gemini hat uns beim Strukturieren des Projekts, beim Finden von logischen Fehlern (z. B. SQL-Bindings und Routing-Fehlern) sowie bei der finalen Korrektur dieser Projektdokumentation geholfen. Zum Abschluss können wir sagen, dass wir durch diesen Prozess extrem viel gelernt haben. Wir sind zu 80 % zuversichtlich, dass wir ein identisches Projekt beim nächsten Mal komplett ohne KI auf die Beine stellen könnten.