## Hier findet Ihr verschiedene Templates für die "Auswertung". Zur Aktivierung das gewünschte Template einfach in den Ordner "Auswertungen" kopieren.
.
.
.
.
# Erklärungen zu den einzelnen Templates (KI generiert!)

---
# ```wetter.py```
---

## Überblick

Dieses Skript sammelt Wetterdaten und zeigt sie auf einer speziellen Anzeige-App (Awtrix3) an. Es zeigt die Temperatur, den Luftdruck, die Luftdrucktendenz und die Mondphase an. Zusätzlich werden je nach Wetterlage verschiedene Overlays angezeigt, wie z.B. für klaren Himmel, leichten Regen, starken Regen, Sturm, Schnee und Frost.

## Importieren von Funktionen

Zuerst werden die notwendigen Funktionen aus anderen Bibliotheken importiert:

- **awtrix3_send_app**: Diese Funktion sendet die aufbereiteten Daten an die Awtrix3-Anzeige.
- **awtrix3_send_settings**: Diese Funktion sendet die Konfigurationseinstellungen an die Awtrix3-Anzeige.
- **get_mondphase**: Diese Funktion ermittelt die aktuelle Mondphase.
- **get_luftdruck_tendenz**: Diese Funktion ermittelt die Tendenz des Luftdrucks.

## Hauptfunktion

Die Hauptfunktion des Skripts verarbeitet die Wetterdaten und sendet die Ergebnisse an die Awtrix3-Anzeige.

### Schritte im Detail

1. **Luftdrucktendenz aktualisieren**
   - Der aktuelle Luftdruck wird eingelesen und die Tendenz (steigend, fallend, gleichbleibend) wird ermittelt.

2. **Temperatur und Farben festlegen**
   - Die aktuelle Temperatur wird aus den Daten entnommen.
   - Je nach Temperatur wird eine entsprechende Farbe zugewiesen (von violett für sehr kalte Temperaturen bis rot für sehr heiße Temperaturen).

3. **Daten für die Anzeige aufbereiten**
   - Die Daten werden in ein Format gebracht, das von der Awtrix3-Anzeige verstanden wird.
   - Es werden die Temperatur, der Himmelzustand (z.B. "klar", "bewölkt"), der Luftdruck und die Luftdrucktendenz angezeigt.
   - Zusätzlich wird die aktuelle Mondphase angezeigt.

4. **Wetter-Overlays setzen**
   - Abhängig von den Wetterbedingungen wird ein entsprechendes Overlay gesetzt (z.B. "drizzle" für leichten Regen, "snow" für Schnee).
   - Wenn die Temperatur unter 0 Grad liegt, wird ein Frost-Overlay gesetzt.
   - Wenn die Temperatur über 0 Grad liegt und weder Regen noch Schnee gemeldet werden, wird ein "clear"-Overlay gesetzt.
   - Je nach Konfiguration wird das Overlay entweder global oder lokal für die aktuelle Anzeige gesetzt.

5. **Daten an die App senden**
   - Die aufbereiteten Wetterdaten und Overlays werden an die Awtrix3-Anzeige gesendet, um die relevanten Wetterinformationen darzustellen.

## Zusammengefasst

Das Skript liest die aktuellen Wetterdaten aus, berechnet und formatiert die Temperatur, den Luftdruck, die Luftdrucktendenz und die Mondphase. Es legt Farben für die Anzeige fest, je nach Temperatur. Abhängig von den Wetterbedingungen werden verschiedene Overlays gesetzt. Schließlich werden die aufbereiteten Daten an die Awtrix3-Anzeige gesendet, um die relevanten Wetterinformationen darzustellen.


---
# ```wground.py```
---

## Übersicht

Dieses Skript wertet Wetterdaten aus und zeigt Temperatur, Luftdruck, Tendenz und Mondphase an. Außerdem wird Niederschlag erkannt und angezeigt, einschließlich der gesamten Tagesniederschlagsmenge und der Wetterüberlagerungen.

## Importieren von Funktionen

Die benötigten Funktionen werden aus einer Funktionen-Bibliothek importiert:

- **awtrix3_send_app**: Diese Funktion sendet die Daten für die Anzeige an die Awtrix3-App.
- **awtrix3_send_settings**: Diese Funktion sendet Einstellungen an Awtrix3, wie z.B. Wetterüberlagerungen.
- **get_mondphase**: Diese Funktion ruft die aktuelle Mondphase ab.
- **get_luftdruck_tendenz**: Diese Funktion ermittelt die Luftdrucktendenz.

## Hauptfunktion

Die Hauptfunktion `auswertung` verarbeitet die Wetterdaten und bereitet sie für die Anzeige auf dem Awtrix3-Display vor.

### Schritte im Detail

1. **Wetterdaten auswerten**
   - Die aktuellen Wetterdaten werden abgerufen, einschließlich Temperatur, Luftdruck und Niederschlag.

2. **Temperatur und Luftdruck anzeigen**
   - Die Temperatur und der Luftdruck werden in Abhängigkeit ihrer Werte angezeigt.
   - Die Luftdrucktendenz wird berechnet und ebenfalls angezeigt.

3. **Niederschlag erkennen und anzeigen**
   - Niederschlag wird erkannt und entsprechend angezeigt.
   - Zusätzlich wird die gesamte Tagesniederschlagsmenge angezeigt.

4. **Wetterüberlagerungen einbeziehen**
   - Je nach Wetterlage werden passende Überlagerungen wie "clear", "drizzle", "rain", "storm", "snow" und "frost" gesetzt und angezeigt.

## Zusammengefasst

Das Skript analysiert Wetterdaten und zeigt Temperatur, Luftdruck, Niederschlag und Wetterüberlagerungen auf dem Awtrix3-Display an.



---
# ```pv.py```
---

## Übersicht

Dieses Skript verarbeitet PV-Daten (Photovoltaik) und zeigt Informationen wie die aktuelle Leistung, den Tagesertrag und den Ladezustand (SoC) auf einer speziellen Anzeige-App (Awtrix3) an.

## Importieren von Funktionen

Zuerst werden die notwendigen Funktionen aus einer Bibliothek importiert:

- **awtrix3_send_app**: Diese Funktion sendet die aufbereiteten Daten an die Awtrix3-Anzeige.

## Hauptfunktion

Die Hauptfunktion `auswertung` verarbeitet die PV-Daten und sendet die Ergebnisse an die Awtrix3-Anzeige.

### Schritte im Detail

1. **Zuweisung und Anpassung der Werte**
   - Die aktuelle Leistung (Leistung), der Tagesertrag (Tagesertrag) und der Ladezustand (SoC) werden aus den Daten entnommen und ggf. berechnet.
   - Beispielhafte Berechnungen für den Fall, dass zwei Wechselrichter (WR) im Einsatz sind, werden als Kommentar bereitgestellt.

2. **Beispiel für die Verarbeitung von zwei Wechselrichtern**
   - In einem kommentierten Abschnitt wird gezeigt, wie man die Leistung und den Tagesertrag summieren kann, wenn zwei Wechselrichter und zwei dazugehörige Datenbanken im Einsatz sind.
   - Der Ladezustand wird von dem Wechselrichter genommen, an dem der Akku hängt.

3. **Aufbereitung der Daten für die Anzeige**
   - Die Daten werden in ein Format gebracht, das von der Awtrix3-Anzeige verstanden wird.
   - Die Anzeige wird mit verschiedenen Texten und Farben formatiert:
     - **PV:** Die aktuelle Leistung in Watt.
     - **Tag:** Der Tagesertrag in Kilowattstunden.
     - **SOC:** Der Ladezustand in Prozent.

4. **Senden der Daten an Awtrix3**
   - Die aufbereiteten Daten werden an die Awtrix3-Anzeige gesendet, um die relevanten PV-Informationen darzustellen.

## Zusammengefasst

Das Skript liest die aktuellen PV-Daten aus, berechnet und formatiert die Leistung, den Tagesertrag und den Ladezustand. Es bringt die Daten in ein ansprechendes Format und sendet sie an die Awtrix3-Anzeige, um die relevanten PV-Informationen darzustellen.

---
# ```pv2.py```
---


## Übersicht

Dieses Skript verarbeitet PV-Daten (Photovoltaik) und zeigt Informationen wie die aktuelle Leistung, den Tagesertrag und den Ladezustand (SoC) auf einer speziellen Anzeige-App (Awtrix3) an. Je nach aktueller Leistung werden unterschiedliche Datensätze an Awtrix3 gesendet.

## Importieren von Funktionen

Zuerst werden die notwendigen Funktionen aus einer Bibliothek importiert:

- **awtrix3_send_app**: Diese Funktion sendet die aufbereiteten Daten an die Awtrix3-Anzeige.

## Hauptfunktion

Die Hauptfunktion `auswertung` verarbeitet die PV-Daten und sendet die Ergebnisse an die Awtrix3-Anzeige.

### Schritte im Detail

1. **Zuweisung und Anpassung der Werte**
   - Die aktuelle Leistung (Leistung), der Tagesertrag (Tagesertrag) und der Ladezustand (SoC) werden aus den Daten entnommen und ggf. berechnet.

2. **Farben für die Anzeige des Tagesertrags festlegen**
   - Der Tagesertrag wird in Kilowattstunden angezeigt und farblich gekennzeichnet. Die Farben reichen von Grün (hoher Ertrag) bis Rot (niedriger Ertrag).

3. **Farben für die Anzeige des SoC festlegen**
   - Der Ladezustand (SoC) wird in Prozent angezeigt und farblich gekennzeichnet. Die Farben reichen von Grün (voll geladen) bis Rot (niedrig geladen).

4. **Erstellen der Datensätze**
   - **data_app_1**: Wird gesendet, wenn die Leistung ungleich 0 ist. Enthält Informationen über die Leistung, den Tagesertrag und den SoC.
   - **data_app_2**: Wird gesendet, wenn die Leistung gleich 0 ist. Enthält nur Informationen über den Tagesertrag.

5. **Senden der Daten an Awtrix3**
   - Je nach aktueller Leistung wird entweder `data_app_1` oder `data_app_2` an Awtrix3 gesendet.

## Zusammengefasst

Das Skript liest die aktuellen PV-Daten aus, berechnet und formatiert die Leistung, den Tagesertrag und den Ladezustand. Es bringt die Daten in ein ansprechendes Format und sendet sie an die Awtrix3-Anzeige, um die relevanten PV-Informationen darzustellen. Dabei wird je nach aktueller Leistung ein unterschiedlicher Datensatz gesendet.


---
# ```soc.py```
---

## Übersicht

Dieses Skript verarbeitet den Ladezustand (State of Charge, SOC) und zeigt ihn auf der Awtrix3-Anzeige an. Abhängig vom SOC-Wert werden unterschiedliche Icons und Farben verwendet, um den aktuellen Ladezustand visuell darzustellen.

## Importieren von Funktionen

Zuerst wird die notwendige Funktion aus einer Bibliothek importiert:

- **awtrix3_send_app**: Diese Funktion sendet die aufbereiteten Daten an die Awtrix3-Anzeige.

## Hauptfunktion

Die Hauptfunktion `auswertung` verarbeitet den SOC-Wert und sendet die Ergebnisse an die Awtrix3-Anzeige.

### Schritte im Detail

1. **Zuweisung des SOC-Werts**
   - Der SOC-Wert wird aus den Daten entnommen und in eine Integer-Variable (`SOC`) konvertiert.

2. **Auswahl des Icons und der Farbe je nach SOC-Wert**
   - Je nach Höhe des SOC-Werts wird ein spezifisches Icon und eine Farbe zugewiesen:
     - SOC == 0: Icon 12832, Farbe #ad0b0b (rot)
     - SOC <= 21: Icon 6359, Farbe #e56d17 (orange)
     - SOC <= 41: Icon 6360, Farbe #d8a90c (dunkelgelb)
     - SOC <= 61: Icon 6361, Farbe #f4ea1f (gelb)
     - SOC <= 81: Icon 6362, Farbe #b6e61a (hellgrün)
     - SOC <= 99: Icon 6363, Farbe #2cf046 (grün)

3. **Aufbereitung der Daten für die Anzeige in der App**
   - Die aufbereiteten Daten enthalten den SOC-Wert als Text, eine Progressbar, das ausgewählte Icon und die Farbe.

4. **Senden der Daten an Awtrix3**
   - Die aufbereiteten Daten werden an Awtrix3 gesendet, um den SOC-Wert anzuzeigen.

## Zusammengefasst

Das Skript liest den aktuellen SOC-Wert aus, bestimmt basierend auf diesem Wert das passende Icon und die Farbe, bereitet die Daten auf und sendet sie an die Awtrix3-Anzeige, um den Ladezustand visuell darzustellen.



---
# ```crypto.py```
---

## Übersicht

Dieses Skript verarbeitet die Daten von Kryptowährungen und zeigt den aktuellen Preis sowie die prozentualen Änderungen in den letzten 24 Stunden und in der letzten Stunde auf der Awtrix3-Anzeige an.

## Importieren von Funktionen

Zuerst wird die notwendige Funktion aus einer Bibliothek importiert:

- **awtrix3_send_app**: Diese Funktion sendet die aufbereiteten Daten an die Awtrix3-Anzeige.

## Hauptfunktion

Die Hauptfunktion `auswertung` verarbeitet die Kryptowährungsdaten und sendet die Ergebnisse an die Awtrix3-Anzeige.

### Schritte im Detail

1. **Initialisierung der `data_app`-Struktur**
   - Die `data_app`-Struktur wird initialisiert, um die Daten für die Anzeige zu speichern. Diese Struktur enthält das Icon, das Push-Icon und den Text, der angezeigt werden soll.

2. **Hinzufügen der Kryptowährungsdaten**
   - Die Funktion durchläuft die `data`-Datenstruktur und verarbeitet die Einträge:
     - Für jeden Eintrag, dessen Schlüssel auf `_0` endet (aktueller Preis), wird die entsprechende Änderung in den letzten 24 Stunden (`_1`) und in der letzten Stunde (`_2`) ermittelt.
     - Die Farbe wird basierend auf der prozentualen Änderung in den letzten 24 Stunden bestimmt (grün für positive und rot für negative Werte).
     - Die Daten werden in die `data_app["text"]`-Liste eingefügt.

3. **Senden der Daten an Awtrix3**
   - Die aufbereiteten Daten werden an Awtrix3 gesendet, um die Kryptowährungsdaten anzuzeigen.

## Zusammengefasst

Das Skript liest die aktuellen Preise und prozentualen Änderungen der Kryptowährungen aus, bereitet diese Daten auf und sendet sie an die Awtrix3-Anzeige, um sie dort darzustellen.


---
# ```auto.py```
---

## Übersicht

Dieses Skript wertet die Daten von Automationsrelais und deren zugehörigen Kontakten aus und zeigt die aktiven Relais und deren Zustände auf der Awtrix3-Anzeige an.

## Importieren von Funktionen

Die erforderliche Funktion wird aus einer Bibliothek importiert:

- **awtrix3_send_app**: Diese Funktion sendet die aufbereiteten Daten an die Awtrix3-Anzeige.

## Hauptfunktion

Die Hauptfunktion `auswertung` verarbeitet die Automationsdaten und sendet die Ergebnisse an die Awtrix3-Anzeige.

### Schritte im Detail

1. **Durchlaufen der Relais und Kontakte**
   - Das Skript durchläuft alle Relais.
   - Für jedes aktive Relais werden die zugehörigen Kontakte überprüft.
   - Wenn ein Kontakt aktiv ist, wird seine Statusfarbe auf grün gesetzt, sonst auf rot.

2. **Aufbereiten der Daten**
   - Ein Text-Array wird erstellt, das die Texte und Farben für die aktiven Relais und Kontakte enthält.

3. **Erstellen der `data_app`-Struktur**
   - Wenn Daten vorhanden sind, wird die `data_app`-Struktur erstellt, um die Daten für die Anzeige zu speichern.
   - Andernfalls wird ein leeres Dictionary erstellt.

4. **Senden der Daten an Awtrix3**
   - Die aufbereiteten Daten werden an Awtrix3 gesendet, um die aktiven Relais und deren Kontakte anzuzeigen.

## Zusammengefasst

Das Skript liest die Daten von Automationsrelais und deren Kontakten aus, identifiziert die aktiven Relais und deren Zustände und sendet diese Informationen an die Awtrix3-Anzeige, um sie dort darzustellen.


---
# ```auto1r1k.py```
---

## Übersicht

Dieses Skript wertet die Daten von einem Automationsrelais und seinem zugehörigen Kontakt aus, sowie die aktuellen Tasmota-Daten wie die Momentanleistung und die Summe des Tagesverbrauchs.

## Importieren von Funktionen

Die erforderliche Funktion wird aus einer Bibliothek importiert:

- **awtrix3_send_app**: Diese Funktion sendet die aufbereiteten Daten an die Awtrix3-Anzeige.

## Hauptfunktion

Die Hauptfunktion `auswertung` verarbeitet die Automationsdaten und Tasmota-Daten und sendet die Ergebnisse an die Awtrix3-Anzeige.

### Schritte im Detail

1. **Überprüfen der Aktivität des Relais**
   - Das Skript überprüft, ob das Relais aktiv ist.
   - Wenn das Relais aktiv ist, werden die Daten für das Relais und den Kontakt sowie die Tasmota-Daten abgerufen.

2. **Aufbereiten der Daten**
   - Ein Text-Array wird erstellt, das die Texte und Farben für das Relais, den Kontakt und die Tasmota-Daten enthält.

3. **Erstellen der `data_app`-Struktur**
   - Wenn Daten vorhanden sind, wird die `data_app`-Struktur erstellt, um die Daten für die Anzeige zu speichern.
   - Andernfalls wird ein leeres Dictionary erstellt.

4. **Senden der Daten an Awtrix3**
   - Die aufbereiteten Daten werden an Awtrix3 gesendet, um das aktive Relais, den Kontakt und die Tasmota-Daten anzuzeigen.

## Zusammengefasst

Das Skript liest die Daten von einem Automationsrelais und seinem Kontakt sowie von Tasmota ab, identifiziert die aktiven Daten und sendet diese Informationen an die Awtrix3-Anzeige, um sie dort darzustellen.



---
# ```indikator.py```
---

## Übersicht

Dieses Skript wertet verschiedene Indikatoren aus und steuert die Anzeige entsprechend. Die Indikatoren umfassen Informationen wie den Ladestrom, die Raspberry Pi-Temperatur und den Betriebsmodus.

## Importieren von Funktionen

Die benötigten Funktionen werden aus einer Funktionen-Bibliothek importiert:

- **awtrix3_send_indikator**: Diese Funktion steuert die Anzeige von Indikatoren auf dem Awtrix3-Display.
- **awtrix3_send_notifikation**: Diese Funktion sendet Benachrichtigungen an das Awtrix3-Display.

## Hauptfunktion

Die Hauptfunktion `auswertung` verarbeitet die Daten der Indikatoren und steuert die Anzeige entsprechend.

### Schritte im Detail

1. **Indikator 1 - Lade- oder Entladestrom**
   - Der Strom wird überprüft, um festzustellen, ob geladen oder entladen wird.
   - Je nach Zustand wird die Farbe des Indikators angepasst.

2. **Indikator 2 - Raspberry Pi-Temperatur**
   - Die Temperatur des Raspberry Pi wird überprüft.
   - Basierend auf der Temperatur wird die Farbe und das Blinken des Indikators angepasst.

3. **Indikator 3 - Betriebsmodus**
   - Der Betriebsmodus wird überprüft, um den Zustand des Systems zu bestimmen.
   - Je nach Modus wird die Farbe des Indikators angepasst.
   - Bei einem Fehlermodus wird eine Benachrichtigung gesendet.

## Zusammengefasst

Das Skript überwacht verschiedene Indikatoren wie den Ladestrom, die Raspberry Pi-Temperatur und den Betriebsmodus. Basierend auf diesen Informationen steuert es die Anzeige der Indikatoren auf dem Awtrix3-Display.



---
# ```raspi.py```
---

## Übersicht

Dieses Skript wertet die Raspberry Pi-Temperatur und den verfügbaren Speicherplatz aus und zeigt die Informationen auf dem Awtrix3-Display an.

## Importieren von Funktionen

Die benötigte Funktion wird aus einer Funktionen-Bibliothek importiert:

- **awtrix3_send_app**: Diese Funktion sendet die Daten für die Anzeige an die Awtrix3-App.

## Hauptfunktion

Die Hauptfunktion `auswertung` verarbeitet die Daten der Raspberry Pi-Temperatur und des freien Speichers und bereitet sie für die Anzeige auf.

### Schritte im Detail

1. **Temperaturanzeige**
   - Die Temperatur des Raspberry Pi wird abgerufen.
   - Die Schriftfarbe wird entsprechend der Temperatur festgelegt.

2. **Anzeige des freien Speichers**
   - Der verfügbare Speicherplatz des Raspberry Pi wird abgerufen.
   - Die Schriftfarbe wird entsprechend des verfügbaren Speichers festgelegt.

## Zusammengefasst

Das Skript überwacht die Raspberry Pi-Temperatur und den verfügbaren Speicherplatz und zeigt die Informationen auf dem Awtrix3-Display an.



---
