""" Auswertung PV-Daten und Anzeige Leistung, Tagesertrag und SOC"""

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import (
    awtrix3_send_app,
)


def auswertung(app, data, config):
    """Auswertung PV-Daten und Anzeige Leistung, Tagesertrag und SOC"""

    # Zuweisung und mögliche Berechnungen und Anpassung der Werte

    Leistung = str(int(data["pv_solaranzeige_Leistung"]))
    Tagesertrag = str(round(float(data["pv_solaranzeige_Wh_GesamtHeute"] / 1000), 2))
    SOC = str(int(data["pv_solaranzeige_SOC"]))

    """
    # Beispiel mit Summen bei Einsatz 2 WR und 2 dazugehörigen Datenbanken (WR-1 WR-2)
    Leistung = str(int(
            data["pv_WR-1_Leistung"]
            + data["pv_WR-2_Leistung"]
        ))

    Tagesertrag = str(round((
                float(data["pv_WR-1_Wh_GesamtHeute"])
                + float(data["pv_WR-2_Wh_GesamtHeute"])
            ) / 1000, 2))

    # SOC vom WR an dem der Akku hängt
    SOC = str(data["pv_WR-1_SOC"])

    """

    # Aufbereitung der Daten für die Anzeige in der App
    data_app = {
        "text": [
            {"t": " PV: ", "c": "#fcff33"},
            {"t": Leistung + " W", "c": "#00ff00"},
            {"t": " + ", "c": "#ed7d3b"},
            {"t": "Tag: ", "c": "#fcff33"},
            {"t": Tagesertrag + " kWh", "c": "#00ff00"},
            {"t": " + ", "c": "#ed7d3b"},
            {"t": "SOC ", "c": "#fcff33"},
            {"t": SOC + " %", "c": "#00ff00"},
        ],
        "icon": 27283,
        "pushIcon": 2,
        "progress": int(SOC),
        "progressc": "#00ff00",
    }

    # Senden der Daten an Awtrix3
    awtrix3_send_app(
        config["awtrix3"]["url"],
        app,
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )
