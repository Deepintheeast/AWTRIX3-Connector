""" Auswertung der Daten und Anzeige auf dem AWTRIX3 

Version 0.1.0
"""
from funktionen import (
    awtrix3_send_app,
    awtrix3_send_settings,
    awtrix3_send_indikator,
    awtrix3_send_notifikation,
    LuftdruckTendenz,
    get_mondphase
)

# diverse Werte setzen
luftdruck_tendenz = LuftdruckTendenz()
fehler_aufgetreten = False


def auswertung(app, data, config):
    """Funktion zur Auswertung der Daten und Anzeige auf dem AWTRIX3"""

#
# Ab hier können/müssen die Auswertungen für die verschiedenen Apps angepasst werden.
#
# Bitte beachten Sie die Kommentare und Hinweise im Programm.
# "Einrückungen" an Anfang der Zeilen sind in Python Bestandteil der Programmierung,
# also "wichtig" und dürfen nicht verändert werden!!!
#

    if app == "wetter":
        # Auswertung Wetterdaten und Anzeige Temperatur, Luftdruck, Tendenz und Mondphase,
        # aktivierung "Wetter-Overlays"
        #
        luftdruck_tendenz.luftdruck_aktualisieren(str(data["wetter_Luftdruck"]))
        # Ermitteln Tendenz Luftdruck
        tendenz = luftdruck_tendenz.ermitteln_tendenz()
        print("Tendenz Luftdruck: ", tendenz)

        temp = data["wetter_Temperatur"]
        # Farbe in Abhängigkeit der Temperatur festlegen
        if temp <= -12:
            hex_color = '#D977DF'
        elif temp <= -6:
            hex_color = '#9545BC'
        elif temp <= -1:
            hex_color = '#4B379C'
        elif temp <= 0:
            hex_color = '#656cee'
        elif temp <= 4:
            hex_color = '#31B8DB'
        elif temp <= 10:
            hex_color = '#31db8c'
        elif temp <= 15:
            hex_color = '#55aa18'
        elif temp <= 21:
            hex_color = '#FFFF28'
        elif temp <= 27:
            hex_color = '#F87E27'
        elif temp <= 32:
            hex_color = '#CF3927'
        else:
            hex_color = '#ff0000'

        data_app = {
            "text": [
                #{"t": " Wetter: ", "c": "#fcff33"},
                {"t":" " + str(temp) + "°C", "c": hex_color},
                {"t": " + ", "c": "#ed7d3b"},
                {
                    "t": str(data["wetter_Himmel"])[0].lower()
                    + str(data["wetter_Himmel"])[1:],
                    "c": "#0033ff",
                },
                {"t": " + ", "c": "#ed7d3b"},
                # {"t": "Luftdruck ", "c": "#00DDDD"},
                {"t": str(int(data["wetter_Luftdruck"])) + " hPa ", "c": "#00DDDD"},
                {"t": tendenz.lower(), "c": "#00DDDD"},
                {"t": " + ", "c": "#ed7d3b"},
                {"t": get_mondphase() , "c": "#f6e95f"},
            ],
            "icon": "weather",
            "pushIcon": 2,
        }

        # Overlay "clear, drizzle, rain, storm, snow, frost" setzen
        if config.getboolean("wetter", "overlay"):
            data_overlay = {}
            if "Leichter Regen" in data["wetter_Himmel"]:
                data_overlay = {"overlay": "drizzle"}
            elif "Mäßiger Regen" in data["wetter_Himmel"]:
                data_overlay = {"overlay": "rain"}
            elif "Starker Regen" in data["wetter_Himmel"]:
                data_overlay = {"overlay": "storm"}
            elif "Schnee" in data["wetter_Himmel"]:
                data_overlay = {"overlay": "snow"}
            elif temp < 0:
                data_overlay = {"overlay": "frost"}
            elif (temp > 0 and "Regen" not in str(data["wetter_Himmel"])
                and "Schnee" not in str(data["wetter_Himmel"])):
                data_overlay = {"overlay": "clear"}
            if  config.getboolean("wetter", "overlay_global"):
                data_overlay["OVERLAY"] = data_overlay["overlay"]
                del data_overlay["overlay"]
                print("Overlay global: ", data_overlay)
                awtrix3_send_settings(config["awtrix3"]["url"], data_overlay)
            else:
                print("Overlay local: ", data_overlay)
                data_app.update(data_overlay)

        awtrix3_send_app(
            config["awtrix3"]["url"],
            app,
            data_app,
            config["settings"]["app_scroll_duration"],
            config["settings"]["app_show_time"],
        )


    elif app == "pv":
        # Auswertung PV-Daten, Anzeige Leistung, Tagesertrag und SOC
        #
        data_app = {
            "text": [
                {"t": " PV: ", "c": "#fcff33"},
                {"t": str(int(data["pv_Leistung"])) + " W", "c": "#00ff00"},
                {"t": " + ", "c": "#ed7d3b"},
                {"t": "Tag: ", "c": "#fcff33"},
                {"t": str(round(float(data["pv_Wh_GesamtHeute"] / 1000), 2)) + " kWh",
                 "c": "#00ff00"},
                {"t": " + ", "c": "#ed7d3b"},
                {"t": "SOC ", "c": "#fcff33"},
                {"t": str(int(data["pv_SOC"])) + " %", "c": "#00ff00"},
            ],
            "icon": 27283,
            "pushIcon": 2,
            "progress": int(data["pv_SOC"]),
            "progressc": "#00ff00",
        }
        awtrix3_send_app(
            config["awtrix3"]["url"],
            app,
            data_app,
            config["settings"]["app_scroll_duration"],
            config["settings"]["app_show_time"],
        )

    elif app == "indikator":
        # Auswertung Indikatoren
        # Indikator 1: Lade(strom) (grün) oder Entlade(strom) (rot)
        # Indikator 2: Temperatur Raspi (grün < 35°C, orange 36°C-50°C, rot >= 50°C)
        # Indikator 3: Betriebsmodus (Batterie (grün), Netz (blau), Fehler(rot))
        # und Notifikation bei Fehler
        #
        global fehler_aufgetreten

        indi1_data = {None}
        if (data["indikator_Strom"]) == 0 and (data["indikator_Entladestrom"]) == 0:
            indi1_data = {"color": "#000000"}
        elif (data["indikator_Entladestrom"]) > 0:
            indi1_data = {
                "color": "#ff0000",
                # "blink": 1200
                # "fade": 5000,
            }
        elif (data["indikator_Strom"]) > 0:
            indi1_data = {
                "color": "#00ff00",
                # "blink": 1200
                # "fade": 5000,
            }
        awtrix3_send_indikator(config["awtrix3"]["url"], 1, indi1_data)

        indi2_data = {None}
        if str((data["indikator_RaspiTemp"])) <= "str(35)":
            indi2_data = {"color": "#00ff00", "fade": 5000}
        elif str((data["indikator_RaspiTemp"])) >= str(36) and (
            str(data["indikator_RaspiTemp"])
        ) <= str(50):
            indi2_data = {"color": "#f1b953", "fade": 3000}
        elif str((data["indikator_RaspiTemp"])) >= str(51):
            indi2_data = {"color": "#ff0000", "blink": 200}
        awtrix3_send_indikator(config["awtrix3"]["url"], 2, indi2_data)

        indi3_data = {None}
        if str(int((data["indikator_IntModus"]))) == "3":  # Batteriemodus
            indi3_data = {"color": "#00ff00"}
        elif str(int((data["indikator_IntModus"]))) == "4":  # Line(Netz)modus
            indi3_data = {"color": "#0000ff"}
        elif str(int((data["indikator_IntModus"]))) == "5":  # Error(Fehler)modus
            indi3_data = {"color": "#ff0000", "blink": 100}
            if not fehler_aufgetreten:
                notifi_data = {
                    "text": "Achtung! Wechselrichter befindet sich im Fehlermodus! Bitte überprüfen! ",
                    "color": "#ff0000",
                    "hold": bool(1),
                }
                awtrix3_send_notifikation(config["awtrix3"]["url"], notifi_data)
                fehler_aufgetreten = True
        awtrix3_send_indikator(config["awtrix3"]["url"], 3, indi3_data)


    elif app == "soc":
        # Auswertung SOC mit unterschiedlichen Icons und Farben je nach Wert
        # und Anzeige des aktuellen SOC als Progressbar (Balken)
        #
        icon = 0
        color = "#ad0b0b"
        if int(float(data["soc_SOC"])) == 0:
            icon = 12832
            color = "#ad0b0b"
        elif int(float(data["soc_SOC"])) <= 21:
            icon = 6359
            color = "#e56d17"
        elif int(float(data["soc_SOC"])) <= 41:
            icon = 6360
            color = "#d8a90c"
        elif int(float(data["soc_SOC"])) <= 61:
            icon = 6361
            color = "#f4ea1f"
        elif int(float(data["soc_SOC"])) <= 81:
            icon = 6362
            color = "#b6e61a"
        elif int(float(data["soc_SOC"])) <= 99:
            icon = 6363
            color = "#2cf046"
        data_app = {
            "text": str(int(data["soc_SOC"])) + " %",
            "progress": (data["soc_SOC"]),
            "progressc": "#00ff00",
            "icon": icon,
            "color": color,
            }
        awtrix3_send_app(
            config["awtrix3"]["url"],
            app,
            data_app,
            config["settings"]["app_scroll_duration"],
            config["settings"]["app_show_time"],
            )

    elif app == "auto1r1k":
        # Auswertung Automation für 1 Relais 1 Kontakt mit
        # aktuellen Tasmota Daten Momentanleistung und Summe Tagesverbrauch
        #
        text = []
        if bool(data[f"auto1r1k_Relais1aktiv"]):
            relais_name = data.get(f"auto1r1k_Relais1Name", "")
            text.append({"t": f" Relais 1 {relais_name} ", "c": "#c3ff00"})
            color = "#00ff00" if int(data[f"auto1r1k_Relais1Kontakt1"]) else "#ff0000"
            text.append({"t": str(int(data[f"auto1r1k_Relais1Kontakt1"])), "c": color})
            tasmota_power = data.get("auto1r1k_tasmota_Power", "")
            text.append({"t": f" akt. Energie {tasmota_power} W", "c": "#002fff"})
            tasmota_tag_power = data.get("auto1r1k_tasmota_Today", "")
            text.append({"t": f" gesamt Tag {tasmota_tag_power} kWh", "c": "#9a8f16"})

            if text:
                for item in text:
                    item["t"] = " " + item["t"]

            data_app = {
                "text": text,
                "icon": "automation",
                "pushIcon": 2,
            }
        else:
            data_app = {}

        awtrix3_send_app(
            config["awtrix3"]["url"],
            app,
            data_app,
            config["settings"]["app_scroll_duration"],
            config["settings"]["app_show_time"],
        )


    elif app == "auto":
        # Auswertung Automation universal für x Relais und x Kontakte
        # Es werden die aktiven Relais und deren Kontakte angezeigt
        # 0 = aus, 1 = ein
        text = []
        for j in range(1, 3):  # 3 = Anzahl der Relais + 1
            if bool(data[f"auto_Relais{j}aktiv"]):
                # Fügen Sie den Text für das Relais und seinen Namen hinzu
                relais_name = data.get(f"auto_Relais{j}Name", "")
                text.append({"t": f" Relais {j} {relais_name} ", "c": "#c3ff00"})
                # Fügen Sie die Werte der aktiven Kontakte hinzu
                num_contacts = int(data[f"auto_Relais{j}AnzKontakte"])
                for i in range(1, num_contacts + 1):
                    color = "#00ff00" if int(data[f"auto_Relais{j}Kontakt{i}"]) else "#ff0000"
                    text.append({"t": str(int(data[f"auto_Relais{j}Kontakt{i}"])), "c": color})        # Erstellen Sie das Dictionary nur, wenn Text vorhanden ist
        if text:
            for item in text:
                item["t"] = " " + item["t"]

            data_app = {
                "text": text,
                "icon": "automation",
                "pushIcon": 2,
            }
        else:
            data_app = {}

        awtrix3_send_app(
            config["awtrix3"]["url"],
            app,
            data_app,
            config["settings"]["app_scroll_duration"],
            config["settings"]["app_show_time"],
        )

    elif app == "crypto":
        # Auswertung Anzeige Kryptowährungen
        # 1. Wert: aktueller Preis in Euro,
        # 2. Wert: 24h-Änderung in %,
        # 3. Wert: letzte Stunde-Änderung in %
        data_app = {
            "icon": 48432,
            "pushIcon": 1,
            #"background": "#02220a",
            "text": [],  # Initialisieren "text" als leere Liste
        }

        # Crypto-Daten hinzufügen
        for key, value in data.items():
            if key.endswith('_0'):
                color = "#00ff00" if data[key[:-1] + '1'] >= 0 else "#ff0000"
                data_app["text"].extend([
                    {"t": f" {key.split('_')[1]}: ", "c": "#ddff33"},
                    {"t": f"{str(value)} € ", "c": color},
                    {"t": " + ", "c": "#ed7d3b"},
                    {"t": f" {str(data[key[:-1] + '1'])} % ", "c": color},
                    {"t": " + ", "c": "#ed7d3b"},
                    {"t": f" {str(data[key[:-1] + '2'])} % ", "c": color}
                ])
        awtrix3_send_app(
            config["awtrix3"]["url"],
            app,
            data_app,
            config["settings"]["app_scroll_duration"],
            config["settings"]["app_show_time"],
        )

    # Hier können Auswertungen für weitere Apps hinzugefügt werden


    # Ab hier nichts mehr ändern
    else:
        print("Nope: Keine Auswertung für App \"" + app + "\" gefunden!")
