""" Auswertung PV-Daten und Anzeige Leistung, Tagesertrag und SOC
in Abhängigkeit der Leistung werden verschiedene Datensets an Awtrix3 gesendet"""

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import (
    awtrix3_send_app,
)

def auswertung(app, data, config):
    """Auswertung PV-Daten und Anzeige Leistung, Tagesertrag und SOC"""
    # verwendete Icons 51301 und 27283

    # Zuweisung und mögliche Berechnungen und Anpassung der Werte
    Leistung = str(int(data["pv2_solaranzeige_Leistung"]))
    Tagesertrag = round(float(data["pv2_solaranzeige_Wh_GesamtHeute"] / 1000), 2)
    SOC = str(int(data["pv2_Pylontech_SOC"]))

    # Aufbereitung der Daten für die Anzeige in der App
    # Farben für die Anzeige des Tagesertrags festlegen
    # hier für den Bereich von 0 bis 35 kWh, bitte anpassen
    if Tagesertrag >= 35:
        color_Tagesertrag = "#2cf046"
    elif Tagesertrag >= 28:
        color_Tagesertrag = "#b6e61a"
    elif Tagesertrag >= 21:
        color_Tagesertrag = "#f4ea1f"
    elif Tagesertrag >= 14:
        color_Tagesertrag = "#d8a90c"
    elif Tagesertrag >= 7:
        color_Tagesertrag = "#e56d17"
    else:
        color_Tagesertrag = "#ad0b0b"

    # wird gesendet wenn Leistung ungleich 0
    data_app_1 = {
        "text": [
            {"t": " PV: ", "c": "#fcff33"},
            {"t": Leistung + " W", "c": "#00ff00"},
            {"t": " + ", "c": "#ed7d3b"},
            {"t": "Tag: ", "c": "#fcff33"},
            {"t": str(Tagesertrag) + " kWh", "c": color_Tagesertrag},
            {"t": " + ", "c": "#ed7d3b"},
            {"t": "SOC ", "c": "#fcff33"},
            {"t": SOC + " %", "c": "#00ff00"},
        ],
        "icon": 27283,
        "pushIcon": 2,
        "progress": SOC,
        "progressc": "#00ff00",
    }

    # wird gesendet wenn Leistung gleich 0
    data_app_2 = {
        "text": [
            {"t": "Tagesertrag: ", "c": "#fcff33"},
            {"t": str(Tagesertrag) + " kWh", "c": color_Tagesertrag},
            #{"t": " + ", "c": "#ed7d3b"},
            #{"t": "SOC ", "c": "#fcff33"},
            #{"t": SOC + " %", "c": "#00ff00"},
        ],
        "icon": 51301,
        "pushIcon": 2,
        "progress": SOC,
        "progressc": "#00ff00",
    }

    # Senden der Daten an Awtrix3 in Abhängigkeit der Leistung
    data_app = data_app_1 if Leistung != "0" else data_app_2
    awtrix3_send_app(
        config["awtrix3"]["url"],
        app,
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )
