
## AWTRIX3-Connector

AWTRIX3-Connector ->
Das Script dient als universelle Schnittstelle für die Darstellung von Informationen aus diversen 
Datenquellen auf Geräten mit der AWTRIX3-Firmware minimum Version 0.96.

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


### Installation

Um die Installation möglichst einfach zu gestalten gibt es ein Installationsscript welches alle erforderlichen Aktionen vornimmt!

Zur Installation bitte als "normaler User" auf einer Konsole an Eurer "Linux Installation" (zB. Solaranzeige) anmelden!

Als erstes müssen wir das Script runterladen:

```
wget https://raw.githubusercontent.com/Deepintheeast/AWTRIX3-Connector/main/install.sh
```
jetzt einfach das Script aufrufen und durchlaufen lassen:

```
bash ./install.sh
```

Tja, eigentlich war es das schon! 

Es sollten jetzt alle benötigten Programmdaten unter

`/home/"Username"/scripts/AWTRIX3-Connector`

angelegt sein und auch der dazugehörige Dienst wurde schon mit erstellt (aber noch nicht gestartet)!

### Konfiguration/Einstellungen

Alle Einstellungen zum Programm wurden in eine eigene "config.ini" Datei ausgelagert und sollten am besten mit

`mcedit /home/"Username"/scripts/AWTRIX3-Connector/config.ini`

bearbeitet werden! Ihr findet in der "config.ini" entsprechende erklärende Kommentare zu den einzelnen Parametern!



Bevor ihr das Programm zum ersten mal startet bitte den User einmal ab und wieder anmelden! Bei der Installation wurde in der .bashrc ein "alias" angelegt und sollte jetzt auch aktiv sein. Dadurch könnte ihr jetzt durch Aufruf von

```
awtrix3connect
```
das Programm zum "testen" starten.

Beenden mit Strg+C!


Wenn alle Einstellungen richtig vorgenommen sind und alles soweit passt dann erst als Dienst starten !

```
sudo systemctl start awtrix3-connector.service
```



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
