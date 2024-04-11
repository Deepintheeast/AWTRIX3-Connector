"""Klassen und Funktionen für die Anbindung an die Datenbanken und das Senden an AWTRIX3"""

import configparser
import threading
from datetime import datetime, timedelta
from multiprocessing import Value
import sqlite3
import time
import schedule
from influxdb import InfluxDBClient
import mysql.connector
import psycopg2
import requests
import ephem

# Lesen der Konfigurationsdatei
config = configparser.ConfigParser()
config.read("config.ini")

# diverse Werte setzen
version_nr = "0.1.1"

# globale Variable
run_true = Value("b", False)


def aktuelle_zeit():
    """Aktuelle Zeit"""
    return datetime.now().strftime("%H:%M:%S")


def query_database(d_app, d_group, d_config):
    """Routine zum Auslesen der Datenbanken und kombinieren der Daten"""
    # Dictionary zum Speichern der Daten anlegen
    combined_data = {}
    # Führen Sie die Abfragen in der Gruppe aus
    for key in d_config[d_group]:
        # Holen Sie das Flag und die restlichen Informationen
        flag, *info = d_config[d_group][key].split(",")

        if flag == "tasmota":
            flag, info = d_config[d_group][key].split(",", 1)
            info = info.split(',')
            info = (info + ['', ''] * 3)[:5]
            ip, gruppe, wert, user, passwort = info
            result = get_tasmota(ip, gruppe, wert, user, passwort)
            key = f"{d_app}_tasmota_{wert}"
            combined_data[key] = result


        if flag == "crypto":
            flag, info = d_config[d_group][key].split(",", 1)
            info = info.strip('"')
            currencies = info.split(',')
            #print(info)
            # Daten abrufen
            data = get_crypto_course(currencies)
            # Daten zum Daten-Dictionary hinzufügen
            for currency, values in data.items():
                for i, value in enumerate(values):
                    key = f"{d_app}_{currency}_{i}"
                    combined_data[key] = value

        elif flag == "influxdb":
            info = (info + ['', ''] * 3)[:6]
            ip, db, measurement, field, username, password = info
            # Erstellen Sie eine Verbindung zum InfluxDB-Server
            client = InfluxDBClient(host=ip, port=8086, username = username, password = password)
            # Wechsel zur aktuellen Datenbank
            client.switch_database(db)
            # Erstellen der Abfrage
            query = f'SELECT last("{field}") FROM "{measurement}"'
            # Ausführen der Abfrage
            result = client.query(query)
            # Ergebnis zum Daten-Dictionary hinzufügen
            for point in result.get_points():
                # Bezeichner und Feld als Schlüssel im Dictionary
                key = f"{d_app}_{field}"
                combined_data[key] = point["last"]

        elif flag == "sqlite":
            db_name, table, column = info
            # Verbinden mit der SQLite-Datenbank
            conn = sqlite3.connect(db_name)
            # Erstellen eines Cursor'
            cursor = conn.cursor()
            # Erstellen der Abfrage
            # query = f"SELECT {column} FROM {table} ORDER BY ROWID DESC LIMIT 1"
            query = f"SELECT {column} FROM {table} ORDER BY id DESC LIMIT 1"
            # ausführen der Abfrage
            cursor.execute(query)
            # Ergebnis holen
            result = cursor.fetchone()
            if result is not None:
                # Ergebnis zum Daten-Dictionary hinzufügen
                key = f"{d_app}_{column}"
                combined_data[key] = result[0]
            # Schließen der Verbindung
            conn.close()

        elif flag == "mariadb":
            info = (info + ['', ''] * 3)[:6]
            host, db_name, table, column, username, password = info
            # Verbinden mit der MariaDB-Datenbank
            conn = mysql.connector.connect(
                user=username, password=password, host=host, database=db_name
            )
            # Erstellen eines Cursor's
            cursor = conn.cursor()
            # Erstellen der Abfrage
            query = f"SELECT {column} FROM {table} ORDER BY id DESC LIMIT 1"
            # Abfrage ausführen
            cursor.execute(query)
            # Ergebnis holen
            result = cursor.fetchone()
            if result is not None:
                # Ergebnis zum Daten-Dictionary hinzufügen
                key = f"{d_app}_{column}"
                combined_data[key] = result[0]
            # Verbindung schließen
            conn.close()

        elif flag == "postgresql":
            info = (info + ['', ''] * 3)[:6]
            host, db_name, table, column, username, password = info
            # Verbinden mit der PostgreSQL-Datenbank
            conn = psycopg2.connect(
                user=username, password=password, host=host, dbname=db_name
            )
            # Erstellen eines Cursor's
            cursor = conn.cursor()
            # Erstellen der Abfrage
            query = f"SELECT {column} FROM {table} ORDER BY id DESC LIMIT 1"
            # Abfrage ausführen
            cursor.execute(query)
            # Ergebnis holen
            result = cursor.fetchone()
            if result is not None:
                # Ergebnis zum Daten-Dictionary hinzufügen
                key = f"{d_app}_{column}"
                combined_data[key] = result[0]
            # Verbindung schließen
            conn.close()
    return combined_data


def get_sa_su(breite, laenge, sa_korrektur=0, su_korrektur=0):
    """Funktion Abfrage Sonnenaufgang/untergang"""
    # Erzeuge das Observer-Objekt
    observer = ephem.Observer()
    observer.lat = str(breite)
    observer.lon = str(laenge)
    # Bestimme das aktuelle Datum und die aktuelle Zeit
    now = datetime.now()
    # Berechne die Zeiten für Sonnenaufgang und Sonnenuntergang
    sun = ephem.Sun()
    sun_auf = ephem.localtime(observer.next_rising(sun, start=now))
    sun_unter = ephem.localtime(observer.next_setting(sun, start=now))
    # Berücksichtige die Korrekturwerte für Sonnenaufgang und Sonnenuntergang
    sun_auf_korr = sun_auf + timedelta(minutes=sa_korrektur)
    sun_unter_korr = sun_unter + timedelta(minutes=su_korrektur)
    # Konvertiere die Zeiten in String-Format
    sun_auf_str = sun_auf.strftime("%H:%M")
    sun_auf_korr_str = sun_auf_korr.strftime("%H:%M")
    sun_unter_str = sun_unter.strftime("%H:%M")
    sun_unter_korr_str = sun_unter_korr.strftime("%H:%M")
    # Gib die Zeiten als Array von Strings zurück
    return [sun_auf_str, sun_auf_korr_str, sun_unter_str, sun_unter_korr_str]


def get_mondphase():
    """Funktion Abfrage Mondphase"""
    # Erstellen Sie ein 'observer'-Objekt und setzen Sie das Datum auf heute
    observer = ephem.Observer()
    observer.lat = str(config.getfloat("astro", "standort_breite"))
    observer.lon = str(config.getfloat("astro", "standort_laenge"))
    observer.date = ephem.now()
    #print(ephem.now())

    # Erstellen Sie ein 'moon'-Objekt
    moon = ephem.Moon()
    # Setzen Sie das 'moon'-Objekt auf die aktuelle Position des Mondes
    moon.compute(observer)
    # Die Mondphase ist ein Wert zwischen 0 und 1, wobei 0 Neumond und 0.5 Vollmond ist
    # Umwandlung der numerischen Mondphase in eine Beschreibung
    if moon.moon_phase < 0.02:
        status = "Neumond"
    elif moon.moon_phase < 0.5:
        status = "Zunehmend"
    elif moon.moon_phase < 0.52:
        status = "Vollmond"
    else:
        status = "Abnehmend"

    print('Mondphase: ', moon.moon_phase)
    print('Moon phase: ', status)
    return status


def update_astrozeiten():
    """Update der Astrozeiten"""
    global astro_zeiten
    astro_zeiten = get_sa_su(
        config.getfloat("astro", "standort_breite"),
        config.getfloat("astro", "standort_laenge"),
        config.getint("astro", "sa_korrektur"),
        config.getint("astro", "su_korrektur"),
    )
    return astro_zeiten


def ist_on_off_time(start_time, stop_time):
    """Funktion zur Überprüfung, ob die aktuelle Zeit zwischen Start- und Stoppzeit liegt"""
    # Aktuelle Zeit als datetime-Objekt
    now = datetime.now().time()

    # Start- und Stoppzeit als datetime-Objekt
    start = datetime.strptime(start_time, "%H:%M").time()
    stop = datetime.strptime(stop_time, "%H:%M").time()

    # Überprüfen, ob die aktuelle Zeit zwischen Start und Stopp liegt
    if start <= stop:
        return start <= now <= stop
    else:  # Wenn die Stoppzeit in den nächsten Tag fällt
        return start <= now or now <= stop


class Scheduler:
    """Klasse für den Scheduler"""
    def __init__(self, config, start, stop, run_true):
        """Initialisierung des Schedulers"""
        self.conf = config
        self.start = start
        self.stop = stop
        self.run_true = run_true
        #self.astro_zeiten = update_astrozeiten()

    def run_schedule(self):
        """Scheduler laufen lassen"""
        while True:
            schedule.run_pending()
            time.sleep(1)

    def start_stop_update(self):
        """Start- und Stop-Zeit aktualisieren"""
        self.astro_zeiten = update_astrozeiten()
        # Start- und Stop- Zeit setzen
        if self.conf.getboolean("astro", "start_astro"):
            self.start = self.astro_zeiten[1]
            self.stop = self.astro_zeiten[3]
        else:
            self.start = self.conf["settings"]["start_time"]
            self.stop = self.conf["settings"]["stop_time"]

        # Alte Aufgaben löschen
        schedule.clear('start_task')
        schedule.clear('stop_task')
        schedule.clear('sa_task')
        schedule.clear('su_task')

        # AWTRIX3 An/Aus schalten
        schedule.every().day.at(self.start).do(
            awtrix3_an_aus, self.conf["awtrix3"]["url"], 1, self.run_true
        ).tag('start_task')
        schedule.every().day.at(self.stop).do(
            awtrix3_an_aus, self.conf["awtrix3"]["url"], 0, self.run_true
        ).tag('stop_task')

        # Notifikationen für Sonnenaufgang und Sonnenuntergang
        schedule.every().day.at(self.astro_zeiten[0]).do(self.notifikation_sa).tag('sa_task')
        schedule.every().day.at(self.astro_zeiten[2]).do(self.notifikation_su).tag('su_task')


    def notifikation_sa(self):
        """Notifikation Sonnenaufgang"""
        if self.conf.getboolean("astro", "show_sa_su"):
            notify_data = {
                "text": "Und immer wieder geht die Sonne auf! Heute, genau jetzt, um "
                + self.astro_zeiten[0]+" Uhr. ",
                "color": "#fff700",
                "repeat": 2,
                "hold": bool(0),
                "icon": 12758,
                "pushIcon": 0,
                "rtttl": "s:d=4,o=6,b=185:c,p,c,p,c"
            }
        awtrix3_send_notifikation(self.conf["awtrix3"]["url"], notify_data)

    def notifikation_su(self):
        """Notifikation Sonnenuntergang"""
        if self.conf.getboolean("astro", "show_sa_su"):
            notify_data = {
                "text": "Jetzt, Sonnenuntergang um "+self.astro_zeiten[2]+
                " Uhr. Der Tag geht und die Nacht beginnt.",
                "color": "#f0a015",
                "repeat": 2,
                "hold": bool(0),
                "icon": 19070,
                "pushIcon": 0,
                "rtttl": "s:d=4,o=6,b=185:c,p,c,p,c"
            }
        awtrix3_send_notifikation(self.conf["awtrix3"]["url"], notify_data)

    def schedule_tasks(self):
        """Aufgaben für den Scheduler planen"""

        # Aktualisierung der Astrozeiten
        schedule.every().day.at("00:05").do(self.start_stop_update)

        # Helligkeit einstellen
        schedule.every().day.at(self.conf["settings"]["start_daymode"]).do(
            awtrix3_hell_set,
            self.conf["awtrix3"]["url"],
            self.conf["settings"]["helligkeit_daymode"],
        )
        schedule.every().day.at(self.conf["settings"]["start_nightmode"]).do(
            awtrix3_hell_set,
            self.conf["awtrix3"]["url"],
            self.conf["settings"]["helligkeit_nightmode"],
        )

    def start_scheduler(self):
        """Starten des Schedulers in einem eigenen Thread"""
        thread = threading.Thread(target=self.run_schedule)
        thread.start()


class LuftdruckTendenz:
    """Klasse zur Ermittlung der Tendenz der Luftdruckwerte"""

    def __init__(self):
        self.luftdruck_werte = []

    def luftdruck_aktualisieren(self, luftdruck):
        """Aktualisieren der Luftdruckwerte"""
        self.luftdruck_werte.append(luftdruck)
        # Behalten Sie nur die letzten 20 Werte
        self.luftdruck_werte = self.luftdruck_werte[-40:]
        debug_print(self.luftdruck_werte)
    def ermitteln_tendenz(self):
        """Ermitteln der Tendenz der Luftdruckwerte"""
        if len(self.luftdruck_werte) < 40:  # wenn weniger als 40 Werte vorhanden sind
            return "n/a"
        else:
            letzte_werte = list(map(float, self.luftdruck_werte[-20:]))
            vorherige_werte = list(map(float, self.luftdruck_werte[-40:-20]))
            durchschnitt_letzte = sum(letzte_werte) / len(letzte_werte)
            durchschnitt_vorherige = sum(vorherige_werte) / len(vorherige_werte)
            if durchschnitt_letzte > durchschnitt_vorherige:
                return " steigend"
            elif durchschnitt_letzte < durchschnitt_vorherige:
                return " fallend"
            else:
                return " stabil"


def awtrix3_send_request(url, request_data):
    """Basis-Funktion um Daten an AWTRIX3 senden"""
    try:
        response = requests.post(url, json=request_data, timeout=10)
        response.raise_for_status()
        # print("Erfolgreich gesendet: Statuscode =", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Fehler beim Senden der Daten:", e)


def awtrix3_send_settings(url, settings_data):
    """Funktion 'Settings' an AWTRIX3 senden"""
    settings_url = url + "/api/settings"
    awtrix3_send_request(settings_url, settings_data)


def awtrix3_effekt_set(url, trans_effect, trans_effect_time):
    """Übergangseffekte setzen"""
    settings_data = {"TEFF": trans_effect, "TSPEED": trans_effect_time}
    awtrix3_send_settings(url, settings_data)


def awtrix3_send_notifikation(url, notify_data):
    """Funktion 'Notifikation' an AWTRIX3 senden"""
    awtrix3_url = url + "/api/notify"
    print(notify_data)
    awtrix3_send_request(awtrix3_url, notify_data)


def awtrix3_send_app(
    url,
    app_name,
    app_data,
    app_scroll_duration,
    app_show_time,
    app_lifetime=config["settings"]["app_lifetime"],
):
    """Funktion App an AWTRIX3 senden
    inkl. setzen von 'repeat' od. 'duration' in Abhängigkeit der Länge von 'text'"""
    if "duration" in app_data:
        app_data.pop("duration")
    if "repeat" in app_data:
        app_data.pop("repeat")
    if "text" in app_data:
        total_characters = sum(len(item) for item in app_data["text"])
        total_char_t = sum(len(item["t"]) for item in app_data["text"] if isinstance(item, dict) and "t" in item)
        if total_char_t > 6 or total_characters > 6:
            app_data["repeat"] = app_scroll_duration
        else:
            app_data["duration"] = app_show_time
        app_data["lifetime"] = app_lifetime
    debug_print("\nSenden an AWTRIX3: " + aktuelle_zeit() + "\n" + str(app_data))
    awtrix3_url = url + "/api/custom?name=" + app_name
    awtrix3_send_request(awtrix3_url, app_data)


def awtrix3_send_app_raw(url, app_raw_name, app_raw_data):
    """Funktion App 'raw' an AWTRIX3 senden"""
    awtrix3_url = url + "/api/custom?name=" + app_raw_name
    awtrix3_send_request(awtrix3_url, app_raw_data)


def awtrix3_send_indikator(url, indicator_nummer, indicator_data):
    """Funktion 'Indikator' an AWTRIX3 senden"""
    awtrix3_url = url + "/api/indicator" + str(indicator_nummer)
    debug_print(
        "Senden an AWTRIX3: "
        + aktuelle_zeit()
        + "\n"
        + str(indicator_nummer)
        + " "
        + str(indicator_data)
    )
    awtrix3_send_request(awtrix3_url, indicator_data)


def awtrix3_kill_indicator(url, indicator_nummer):
    """Indikatoren löschen einzeln"""
    awtrix3_url = url + "/api/indicator" + str(indicator_nummer)
    indicator_data = {}
    awtrix3_send_request(awtrix3_url, indicator_data)


def awtrix3_kill_all_indicator(url):
    """Indikatoren löschen alle"""
    i = 1
    while i <= 3:
        awtrix3_url = url + "/api/indicator" + str(i)
        indicator_data = {}
        awtrix3_send_request(awtrix3_url, indicator_data)
        i += 1


def awtrix3_an_aus(url, on_off, run_true):
    """Start Funktion AWTRIX3 An/Aus schalten"""
    run_true.value = on_off
    if on_off == 0 and config.getboolean("settings", "night_show"):
        awtrix3_kill_all_indicator(url)
        awtrix3_kill_apps(url)
        awtrix3_switch(url)
        awtrix3_send_settings(
            config["awtrix3"]["url"], {"OVERLAY": "clear"})
        time.sleep(30)
        awtrix3_kill_all_indicator(url)
    else:
        awtrix3_url = url + "/api/power"
        power_data = {
            "power": bool(on_off),
        }
        awtrix3_send_request(awtrix3_url, power_data)


def awtrix3_hell_set(url, helligkeit):
    """Start Helligkeit einstellen"""
    awtrix3_url = url = url + "/api/settings"
    if helligkeit in ["a", "A"]:
        hell_data = {"ABRI": bool(1)}
    else:
        hell_data = {"ABRI": bool(0), "BRI": helligkeit}
    awtrix3_send_request(awtrix3_url, hell_data)


def awtrix3_init():
    """Initialisierung AWTRIX3"""
    awtrix3_an_aus(
        config["awtrix3"]["url"], 1, run_true
    )  # AWTRIX3 (falls aus) einschalten
    awtrix3_kill_all_indicator(config["awtrix3"]["url"])  # Alle Indikatoren löschen
    awtrix3_send_settings(
        config["awtrix3"]["url"], {"OVERLAY": "clear"}
    )  # Overlays "clear"
    #    awtrix3_hell_set(config["awtrix3"]["url"], config["settings"]["helligkeit_daymode"])
    awtrix3_effekt_set(
        config["awtrix3"]["url"],
        config["settings"]["trans_effect"],
        config["settings"]["trans_effect_time"],
    )  # Übergangseffekte setzen
    awtrix3_send_settings(
        config["awtrix3"]["url"], {"SSPEED": config["settings"]["text_scrollspeed"]}
    )  # Textscrollgeschwindigkeit setzen


def get_awtrix_version(url):
    """AWTRIX-Version abrufen und Präsentsstatus überprüfen"""
    # Senden Sie eine GET-Anfrage an die URL
    response = requests.get(url, timeout=10)
    # Überprüfen Sie, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        # Konvertieren Sie die Antwort in JSON
        data = response.json()
        # Holen Sie sich die Version aus den Daten
        version = data.get("version")
        ram = data.get("ram")
        # Geben Sie die Version zurück
        return version, ram
    else:
        print(
            f"Fehler beim Abrufen der Daten von {url}. Status code: {response.status_code}"
        )
        return None


def awtrix3_switch(url):
    """Funktion für das Umschalten der internen Apps"""
    awtrix3_url = url = url + "/api/switch"
    switch_data = {"name": config["settings"]["night_show_app"]}
    awtrix3_send_request(awtrix3_url, switch_data)


def awtrix3_kill_apps(url):
    """Funktion zum Beenden aller Apps"""
    time.sleep(10)
    # Aktive apps aus config [apps] holen
    apps_dict = dict(config.items("apps"))
    # Schleife über alle apps
    for key, value in apps_dict.items():
        awtrix3_url = url + "/api/custom?name=" + key
        kill_data = {}
        awtrix3_send_request(awtrix3_url, kill_data)


def get_crypto_course(currencies):
    """Abfrage der Kryptowährungspreise und -änderungen."""
    url = ('https://min-api.cryptocompare.com/data/pricemultifull'
    '?fsyms={}'
    '&tsyms=EUR'
    '&api_key={}')
    formatted_url = url.format(",".join(currencies), config["crypto"]["api_key"])
    try:
        response = requests.get(formatted_url, timeout=5)
        data = response.json()
        course = {}
        for currency in currencies:
            currency = currency.strip("'")  # Entfernen Sie die Anführungszeichen
            price = round(data['RAW'][currency]['EUR']['PRICE'],1)
            change_pct_24h = round(data['RAW'][currency]['EUR']['CHANGEPCT24HOUR'], 2)
            change_pct_hour = round(data['RAW'][currency]['EUR']['CHANGEPCTHOUR'], 2)
            course[currency] = ( price, change_pct_24h, change_pct_hour)
        return course
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return {}


def debug_print(nachricht):
    """erweiterte Druckausgabe zum Debuggen."""
    if config.getboolean("settings", "debug"):
        print(nachricht)


def get_tasmota(ip, gruppe, wert, user, passwort):
    """
    Holt Daten von einem Tasmota-Gerät.

    :param ip: Die IP-Adresse des Tasmota-Geräts.
    :param gruppe: Die Gruppe der abzurufenden Daten.
    :param wert: Der spezifische Wert, der abgerufen werden soll.
    :param user: Der Benutzername für die Authentifizierung.
    :param passwort: Das Passwort für die Authentifizierung.
    :return: Der abgerufene Wert oder "n/a", wenn ein Fehler auftritt.
    """
    url = f"http://{ip}/cm?cmnd=status%200"
    try:
        response = requests.get(url, auth=(user, passwort), timeout=5)
        data = response.json()
        if gruppe == 'ENERGY':
            return data['StatusSNS'][gruppe][wert]
        elif gruppe.startswith('DS18B20'):
            return data['StatusSNS'][gruppe][wert]
        else:
            return data[gruppe][wert]
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Daten von {ip}: {e}")
        return "n/a"

def intro():
    """Funktion intro"""
    awtrix3_send_settings(
    config["awtrix3"]["url"], {"BRI": 255,"OVERLAY": "clear"}
    )

    notifi_data = {
        "text": " AWTRIX 3 Connector -> Version " + str(version_nr),
        "rainbow": bool(1),
        "rtttl": "s:d=4,o=6,b=185:c,p,c,p,c",
        "repeat": int(1),
    }
    awtrix3_send_notifikation(config["awtrix3"]["url"], notifi_data)
