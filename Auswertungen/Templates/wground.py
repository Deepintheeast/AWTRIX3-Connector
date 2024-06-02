""" Auswertung Wetterdaten und Anzeige Temperatur, Luftdruck, Tendenz und Mondphase,
    sowie Anzeige bei Niederschlag und Anzeige der gesamt Tages-Niederschlagsmenge
    und Anzeige Wetter-Overlays (clear, drizzle, rain, storm, snow, frost)
    
    ACHTUNG: funktioniert nur mit Wetterdaten von Wunderground
    (hier steht wie es geht -> https://github.com/Deepintheeast/wunder2influx)
    
    """

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import awtrix3_send_app, awtrix3_send_settings, get_mondphase, debug_print
from awtrix3connect import get_luftdruck_tendenz

luftdruck_tendenz = get_luftdruck_tendenz()

def auswertung(app, data, config):
    """Beginn der Auswertung für die Wetter-App"""

    # Werte zuweisen und mögliche Berechnungen und Anpassungen der Werte
    niederschlag = data["wground_wunderweather_Niederschlag mm/h"]
    niederschlag_24h = data["wground_wunderweather_Niederschlag 24h"]
    temp = int(data["wground_wunderweather_Temperatur"])
    luftdruck = int(data["wground_wunderweather_Luftdruck"])

    debug_print("Niederschlag: " + str(niederschlag))
    debug_print("Niederschlag 24h: " + str(niederschlag_24h))

    # Ermittlung der Luftdrucktendenz
    luftdruck_tendenz.luftdruck_aktualisieren(str(luftdruck))
    tendenz = luftdruck_tendenz.ermitteln_tendenz()
    debug_print("Tendenz Luftdruck: " + tendenz)

    # Farbe fur Temperaturwert in Abhängigkeit der Temperatur festlegen
    if temp <= -12:
        hex_color = "#D977DF"
    elif temp <= -6:
        hex_color = "#9545BC"
    elif temp <= -1:
        hex_color = "#4B379C"
    elif temp <= 0:
        hex_color = "#656cee"
    elif temp <= 4:
        hex_color = "#31B8DB"
    elif temp <= 10:
        hex_color = "#31db8c"
    elif temp <= 15:
        hex_color = "#55aa18"
    elif temp <= 21:
        hex_color = "#FFFF28"
    elif temp <= 27:
        hex_color = "#F87E27"
    elif temp <= 32:
        hex_color = "#CF3927"
    else:
        hex_color = "#ff0000"

    # Niederschlag in Abhängigkeit der Menge, Anzeige letzte 24h und
    # Overlay "clear, drizzle, rain, storm, snow, frost" setzen
    if 0 < niederschlag < 2.5:
        niederschlag_text = "Nieselregen"
    elif 2.5 <= niederschlag < 10.0:
        niederschlag_text = "leichter Regen"
    elif 10.0 <= niederschlag < 50.0:
        niederschlag_text = "mäßiger Regen"
    elif 50.0 <= niederschlag:
        niederschlag_text = "starker Regen"
    else:
        niederschlag_text = ""

    # Bei negativen Temperaturen "Frost" anzeigen
    if temp < 0:
        if -3 < temp < 0:
            niederschlag_text = "leichter Frost"
        elif -10 <= temp <= -3:
            niederschlag_text = "mittlerer Frost"
        elif temp < -10:
            niederschlag_text = "strenger Frost"
    else:
        niederschlag_text = niederschlag_text

    data_app = {
        "text": [
            {"t": " " + str(temp) + "°C", "c": hex_color},
            {"t": " + ", "c": "#ed7d3b"},
            {
                "t": str(luftdruck) + " hPa ",
                "c": "#00DDDD",
            },
            {"t": tendenz.lower(), "c": "#00DDDD"},
            {"t": " + ", "c": "#ed7d3b"},
            {"t": get_mondphase(), "c": "#f6e95f"},
        ],
        "icon": "weather",
        "pushIcon": 2,
    }

    # Bei Niederschlag Mengen anzeigen
    if niederschlag == 0 and niederschlag_24h > 0:
        data_app["text"].insert(
            5, {"t": " " + str(niederschlag_24h) + "mm/24h", "c": "#272dde"}
        )
        data_app["text"].insert(6, {"t": " + ", "c": "#ed7d3b"})

    if niederschlag > 0 and niederschlag_24h > 0:
        data_app["text"] = [
            {"t": " " + str(temp) + "°C", "c": hex_color},
            {"t": " + ", "c": "#ed7d3b"},
            {
                "t": str(luftdruck) + " hPa ",
                "c": "#00DDDD",
            },
            {"t": tendenz.lower(), "c": "#00DDDD"},
            {"t": " + ", "c": "#ed7d3b"},
            {"t": " " + str(niederschlag_text), "c": "#272dde"},
            {"t": " + ", "c": "#ed7d3b"},
            {"t": " " + str(niederschlag_24h) + "mm/24h", "c": "#272dde"},
            {"t": " + ", "c": "#ed7d3b"},
            {"t": get_mondphase(), "c": "#f6e95f"},
        ]

    # Overlay "clear, drizzle, rain, storm, snow, frost" setzen
    if config.getboolean("wetter", "overlay"):
        data_overlay = {}
        if "Nieselregen" in niederschlag_text:
            data_overlay = {"overlay": "drizzle"}
        elif "leichter Regen" in niederschlag_text:
            data_overlay = {"overlay": "rain"}
        elif (
            "mäßiger Regen" in niederschlag_text or "starker Regen" in niederschlag_text
        ):
            data_overlay = {"overlay": "storm"}
        elif "Schnee" in niederschlag_text:
            data_overlay = {"overlay": "snow"}
        elif "Frost" in niederschlag_text:
            data_overlay = {"overlay": "frost"}
        elif (
            temp > 0
            and "Regen" not in str(niederschlag_text)
            and "Schnee" not in str(niederschlag_text)
            and "Nieselregen" not in str(niederschlag_text)
            and "Frost" not in str(niederschlag_text)
        ):
            data_overlay = {"overlay": "clear"}
        if config.getboolean("wetter", "overlay_global"):
            data_overlay["OVERLAY"] = data_overlay["overlay"]
            del data_overlay["overlay"]
            debug_print("Overlay global: " + str(data_overlay))
            awtrix3_send_settings(config["awtrix3"]["url"], data_overlay)
        else:
            debug_print("Overlay local: " + str(data_overlay))
            data_app.update(data_overlay)

    awtrix3_send_app(
        config["awtrix3"]["url"],
        app,
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )
