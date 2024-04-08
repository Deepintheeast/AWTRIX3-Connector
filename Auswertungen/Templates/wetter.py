""" Auswertung Wetterdaten und Anzeige Temperatur, Luftdruck, Tendenz und Mondphase,
    und Anzeige Wetter-Overlays (clear, drizzle, rain, storm, snow, frost)"""

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import (
    awtrix3_send_app,
    awtrix3_send_settings,
#   LuftdruckTendenz,
    get_mondphase
)
from awtrix3connect import get_luftdruck_tendenz

luftdruck_tendenz = get_luftdruck_tendenz()

def auswertung(app, data, config):
    """ Beginn der Auswertung für die Wetter-App """
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
        "wetter",
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )
