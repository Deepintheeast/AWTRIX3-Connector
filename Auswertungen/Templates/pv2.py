""" Auswertung PV-Daten und Anzeige Leistung, Tagesertrag und SOC
in Abhängigkeit der Leistung werden verschiedene Datensets an Awtrix3 gesendet"""

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import (
    awtrix3_send_app,
)

def auswertung(app, data, config):
    """Auswertung PV-Daten und Anzeige Leistung, Tagesertrag und SOC"""

    # Zuweisung und mögliche Berechnungen und Anpassung der Werte
    leistung = str(int(data["pv2_solaranzeige_Leistung"]))
    tagesertrag = round(float(data["pv2_solaranzeige_Wh_GesamtHeute"] / 1000), 2)
    soc = int(data["pv2_solaranzeige_SOC"])+1

    # Aufbereitung der Daten für die Anzeige in der App
    # Farben für die Anzeige des Tagesertrags festlegen
    # hier für den Bereich von 0 bis 35 kWh, bitte anpassen
    if tagesertrag >= 35:
        color_tagesertrag = "#2cf046"  # grün
    elif tagesertrag >= 28:
        color_tagesertrag = "#b6e61a"
    elif tagesertrag >= 21:
        color_tagesertrag = "#f4ea1f"
    elif tagesertrag >= 14:
        color_tagesertrag = "#d8a90c"
    elif tagesertrag >= 7:
        color_tagesertrag = "#e56d17"
    else:
        color_tagesertrag = "#ad0b0b"  # rot

    # Farben für die Anzeige des SoC festlegen
    # für den Bereich von 0 bis 100% in 20% Schritten
    if soc >= 98:
        color_soc = "#2cf046"  # grün
    elif soc >= 80:
        color_soc = "#b6e61a"
    elif soc >= 60:
        color_soc = "#f4ea1f"
    elif soc >= 40:
        color_soc = "#d8a90c"
    elif soc >= 20:
        color_soc = "#e56d17"
    else:
        color_soc = "#ad0b0b"  # rot

    # data_app_1 -> wird gesendet wenn Leistung ungleich 0
    data_app_1 = {
        "text": [
            {"t": " PV: ", "c": "#fcff33"},
            {"t": leistung + " W", "c": "#00ff00"},
            {"t": " + ", "c": "#ed7d3b"},
            {"t": "Tag: ", "c": "#fcff33"},
            {"t": str(tagesertrag) + " kWh", "c": color_tagesertrag},
            {"t": " + ", "c": "#ed7d3b"},
            {"t": "SOC ", "c": "#fcff33"},
            {"t": str(soc) + " %", "c": color_soc},
        ],
        "icon": 27283,
        "pushIcon": 2,
        "progress": soc,
        "progressC": color_soc,
    }

    # data_app_2 -> wird gesendet wenn Leistung gleich 0
    data_app_2 = {
        "text": [
            {"t": "Tagesertrag: ", "c": "#fcff33"},
            {"t": str(tagesertrag) + " kWh", "c": color_tagesertrag},
            #{"t": " + ", "c": "#ed7d3b"},
            #{"t": "SOC ", "c": "#fcff33"},
            #{"t": str(soc) + " %", "c": color_soc},
        ],
        "icon": 51301,
        "pushIcon": 2,
        "progress": soc,
        "progressC": color_soc,
    }

    # Senden der Daten an Awtrix3 in Abhängigkeit der Leistung
    data_app = data_app_1 if leistung != "0" else data_app_2
    awtrix3_send_app(
        config["awtrix3"]["url"],
        app,
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )
