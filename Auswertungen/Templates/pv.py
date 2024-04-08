""" Auswertung PV-Daten und Anzeige Leistung, Tagesertrag und SOC"""

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import (
    awtrix3_send_app,
)

def auswertung(app, data, config):
    """ Auswertung PV-Daten und Anzeige Leistung, Tagesertrag und SOC"""

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
