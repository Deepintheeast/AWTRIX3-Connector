""" Auswertung Template für einen einzelnen Wert"""

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import awtrix3_send_app

def auswertung(app, data, config):
    # Auswertung Template für einen einzelnen Wert

    # Zuweisung Wert
    WERT = int(data["WERT"])

    # Aufbereitung der Daten für die Anzeige in der App
    data_app = {
        "text": "Bezeichnung: " + str(WERT),   
        "icon": ICON,
        "color": "#00ff00",
    }
    # Senden der Daten an Awtrix3
    awtrix3_send_app(
        config["awtrix3"]["url"],
        app,
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )
