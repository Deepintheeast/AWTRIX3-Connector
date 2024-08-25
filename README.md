
## AWTRIX3-Connector

AWTRIX3-Connector ->
Das Script dient als universelle Schnittstelle für die Darstellung von Informationen aus diversen 
Datenquellen auf Geräten mit der AWTRIX3-Firmware minimum Version 0.96.

Link -> [Projektseite AWTRIX3](https://blueforcer.github.io/awtrix3/#/)

Link -> [Onlineflasher](https://blueforcer.github.io/awtrix3/#/flasher)

Affiliate-Link -> [Ulanzi Pixel Clock](https://www.ulanzi.de/products/ulanzi-pixel-smart-uhr-2882?_pos=1&_psq=pixel&_ss=e&_v=1.0&ref=z6pvugfl)

( bei einem Kauf der Uhr über diesen Link erhalte ich eine kleine Provision die mit zur Finanzierung dieses Projektes genutzt wird! Danke an alle die das so machen/gemacht haben!)


Aktuell können "Daten aus InfluxDB, SQLite, MariaDB, PostgreSQL und von Tasmota-Geräten" 
abgerufen und auf der AWTRIX3-Plattform dargestellt werden. 
Die Daten können sowohl einzeln aus einer Datenquelle oder auch kombiniert von verschiedenen
Quellen abgerufen und weiterverarbeitet werden.

Zusätzlich besteht die Möglichkeit aktuelle "Kurse und Informationen über Cryptowährungen" 
von https://www.cryptocompare.com abzurufen und darzustellen.

Das Script stellt "Astro Informationen" (Sonnenaufgang, Sonnenuntergang, Mondphase) 
zur Darstellung bzw. Steuerung zur Verfügung.

Die Anzeige der Daten erfolgt in Form von Text, Symbolen und Grafiken und kann in Abhängigkeit
von der Tageszeit und anderen Parametern (Astro etc.) gesteuert werden.

```
Version 0.1.0  (07.04.2024)

- Erstveröffentlichung

Version 0.1.1  (11.04.2024)

- Fehler Start/Stopzeit wenn Stop in nächstem Tag behoben
- Auswertung in eigene Module/Dateien (je App) ausgelagert, Templates speziell für
  "Solaranzeige" befinden sich im Ordner "Auswertungen/Templates". Templates entsprechend
  anpassen und zum "aktivieren" in den Ordner "Auswertungen" kopieren. Alle Templates im 
  Ordner "Auswertungen" werden automatisch bei Programmstart geladen.
- Fehler bei der Berechnung der Mondphase behoben
- diverse "kosmetische" Anpassungen

13.04.2024
- Tool "showdb" für InfluxDB hinzugefügt.
Solaranzeige User können sich durch Aufruf von
`showdb "Datenbankname"`
alle letzten Einträge der Datenbank anzeigen lassen. Das hilft die "richtigen Datenbanknamen"
zu finden und das ganze auf Plausibilität zu checken.

19.04.2024

Es gibt leider immer noch ein Fehler in der Mondphasenberechnung!
Fix folgt demnächst, möchte das gern erst noch ein bisschen testen!

Version 0.1.2  (13.05.2024)

- Pausenzeit zwischen den Apps jetzt in config.ini einstellbar
- Anzeige der Uhr (Time) wahlweise 1x im Loop oder nach jeder App möglich
- InfluxDB Portangabe in config.ini nötig/möglich
- Mondphasenberechnung gefixt

Version 0.1.3  (18.05.2024)

- div. Anpassungen 
- Erweiterung der "Variablennamen" um den Namen der Datenbank
  von bisher z.Bsp. "pv_Leistung" -> "pv_solaranzeige_Leistung" als 
  Voraussetzung für's Abholen von Daten aus identischen Datenbanken mit 
  unterschiedlichen Namen (z.Bsp. bei Einsatz von 2 WR (WR-1, WR-2))
- Aktualisierung der Templates und Anpassung des Templates "pv.py" um 
  Beispiel "Berechnungen(Summen) aus Werten mehrerer Datenbanken(WR)"

```

---


### Installation

Um die Installation möglichst einfach zu gestalten gibt es ein Bash-Installationsscript (lauffähig auf Debian basierenden Distributionen) welches alle erforderlichen Aktionen vornimmt! Da es sich beim "AWTRIX3-Connector" um ein reines "Python-Script" handelt sollte es auch problemlos auf anderen Plattformen bis hin zu Windows Installationen mit entsprechend vorhandener "Python-Basis" funktionieren. 
Bei mir läuft es stabil unter Debian auf diversen "Raspberry's" sowie auf einem Debian 12 basierenden Container unter Proxmox.

Zur Installation bitte als "normaler User" auf einer Konsole an Eurer "Linux Installation" (zB. Solaranzeige) anmelden!

Mit folgendem Aufruf wird der "Installer" runtergeladen und ausgeführt:

```
wget https://raw.githubusercontent.com/Deepintheeast/AWTRIX3-Connector/main/install.sh && bash ./install.sh

```

Tja, eigentlich war es das schon! 

Es sollten jetzt alle benötigten Programmdaten unter

`/home/"Username"/scripts/AWTRIX3-Connector`

angelegt sein und auch der dazugehörige Dienst wurde schon mit erstellt (aber noch nicht gestartet)!


---


### Konfiguration/Einstellungen

Alle Einstellungen zum Programm wurden in eine eigene "config.ini" Datei ausgelagert und sollten am besten mit

`mcedit /home/"Username"/scripts/AWTRIX3-Connector/config.ini`

bearbeitet werden! Ihr findet in der "config.ini" entsprechende erklärende Kommentare zu den einzelnen Parametern!



Bevor ihr das Programm zum ersten mal startet bitte mindestens die IP-Adresse Eures AWTRIX (Ulanzi) in der "config.ini" einstellen! Bei der Installation wurde in der .bashrc ein "alias" angelegt und sollte jetzt auch aktiv sein. Dadurch könnte ihr jetzt durch Aufruf von

```
awtrix3connect
```
das Programm zum "testen" starten.

Beenden mit Strg+C!

---


### Start und Handling als Dienst!

Wenn alle Einstellungen richtig vorgenommen sind und alles soweit passt dann erst als Dienst starten !

```
sudo systemctl start awtrix3-connector.service
```
Weitere wichtige Befehle zum Handling des Dienstes sind anstelle von "start" -> "stop" , "restart" oder "status", und sollten selbsterklärend sein!
Wenn ein Dienst läuft und Änderungen durchgeführt wurden muss dieser zur Übernahme der Änderungen "neu gestartet werden!" 
```
sudo systemctl restart awtrix3-connector
```

---


## Installation 2. Instanz

Hat jemand mehr als eine Ulanzi, können zusätzliche Instanzen des Programmes, welche unabhängig voneinander laufen, installiert werden!

Das geht einfach durch wiederholten Aufruf des Scriptes mit Angabe eines Parameters als Name/Nummer etc.

Beispiel:

normaler Aufruf des Scripts mit

`bash ./install.sh`

erzeugt eine Instanz unter 

`/home/"User"/scripts/AWTRIX3-Connector`

ein Aufruf mit Parameter "buero" 

Aufruf des Scripts mit

`bash ./install.sh buero`

erzeugt eine Instanz unter 

`/home/"User"/scripts/AWTRIX3-Connector-buero`

Bitte keine Sonderzeichen, Umlaute, Leerzeichen im "Parameter" verwenden!

Das kann für quasi beliebig viele Instanzen durchgeführt werden!

Es werden auch der jeweilige Dienst unter selbem Schema eingerichtet!
