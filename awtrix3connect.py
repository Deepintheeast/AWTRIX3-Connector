#!/usr/bin/env python3
"""AWTRIX3-Connector ->
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

Version 0.1.0

"""
import configparser
import time
from datetime import datetime
from multiprocessing import Value
from auswertung import auswertung
from funktionen import (
    awtrix3_init,
    awtrix3_hell_set,
    awtrix3_an_aus,
    query_database,
    Scheduler,
    get_mondphase,
    aktuelle_zeit,
    update_astrozeiten,
    ist_on_off_time,
    get_awtrix_version,
    debug_print,
    intro,
)


# Lesen der Konfigurationsdatei
config = configparser.ConfigParser()   
config.read("config.ini")


# global verfügbare Variable
run_true = Value("b", True)

# Ausgabe der Version und Check Erreichbarkeit
status = get_awtrix_version(config["awtrix3"]["url"] + "/api/stats")
print(f"AWTRIX 3 erreichbar, Version: {status[0]}, Ram: {status[1]}")

# Astrozeiten aktualisieren

astro_zeiten = update_astrozeiten()
debug_print("!" + str(astro_zeiten))

debug_print("Mond -> " + get_mondphase())

# Start- und Stop- Zeit setzen
if config.getboolean("astro", "start_astro"):
    start = astro_zeiten[1]
    stop = astro_zeiten[3]
else:
    start = config["settings"]["start_time"]
    stop = config["settings"]["stop_time"]

debug_print(f"Startzeit: {start}, Stopzeit: {stop}")

# Prüfen, ob aktuelle Zeit zwischen start/stop (ON) liegt
if ist_on_off_time(start, stop):
    debug_print("aktuell -> ON")
else:
    debug_print("aktuell -> OFF")
    awtrix3_an_aus(config["awtrix3"]["url"], 0, run_true)  # AWTRIX3 aus


# Erstellen Sie ein Scheduler-Objekt und starten Sie es
scheduler = Scheduler(config, start, stop, run_true)
scheduler.start_stop_update()
scheduler.schedule_tasks()
scheduler.start_scheduler()

# Initialisierung AWTRIX3
awtrix3_init()
intro()

# Vergleiche aktueller Zeit mit Mode-Startzeiten und setzen entsprechender Helligkeit
if (
    config["settings"]["start_daymode"]
    <= aktuelle_zeit()
    < config["settings"]["start_nightmode"]
):
    awtrix3_hell_set(config["awtrix3"]["url"], config["settings"]["helligkeit_daymode"])
    MODE = "Day"
else:
    awtrix3_hell_set(config["awtrix3"]["url"], config["settings"]["helligkeit_nightmode"])
    MODE = "Night"
debug_print(f"Der aktuelle Modus ist {MODE} und die Helligkeit entsprechend gesetzt.\n\n")


# Loop starten

X = True # Hilfsvariablen setzen

while True:

    if run_true.value:
        print("! run_true ist:", run_true.value, "Loop startet...\n")

        for app in config["apps"]:
            Zeit = datetime.now().strftime("%H:%M:%S")
            # Holen der Gruppe von Abfragen für aktuelle app
            group = config["apps"][app]

            # Daten aus den Datenbanken abrufen
            data = query_database(app, group, config)

            # numerische Daten in Float umwandeln, "string bleibt string"
            for key, value in data.items():
                if not isinstance(value, float):
                    try:
                        data[key] = float(value)
                    except ValueError:
                        debug_print(
                            f'Konnte "{value}" nicht in Float umwandeln, '
                            'sollte demnach ein "String" sein'
                        )

            print(f"\033[1mApp: {app}\n\033[0m", data)
            # Funktion "auswertung" aufrufen
            auswertung(app, data, config)

            X = True  # "X" zurücksetzen

            time.sleep(6) # "X" Sekunden Pause vor dem nächsten Durchlauf
            print("\n\n")
    else:
        if X and config.getboolean("settings", "night_show"):
            print("Nightshow aktiviert.\n")
            X = False
        print("Anzeige Aus -> Pause 60 Sekunden - Warten auf Start_Zeit...\n")
        time.sleep(60)  # Pause 60 Sekunden
