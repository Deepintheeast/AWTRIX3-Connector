""" Auswertung SOC mit unterschiedlichen Icons und Farben je nach Wert"""

# Importieren der benötigten Funktionen aus der Funktionen-Bibliothek
from funktionen import awtrix3_send_app

def auswertung(app, data, config):
    # Auswertung SOC mit unterschiedlichen Icons und Farben je nach Wert
    # und Anzeige des aktuellen SOC als Progressbar (Balken)

    #Zuweisung Wert SOC
    SOC = int(data["soc_solaranzeige_SOC"])

    #Auswahl des Icons und der Farbe je nach SOC-Wert
    icon = 0
    color = "#ad0b0b"
    if SOC == 0:
        icon = 12832
        color = "#ad0b0b"
    elif SOC <= 21:
        icon = 6359
        color = "#e56d17"
    elif SOC <= 41:
        icon = 6360
        color = "#d8a90c"
    elif SOC <= 61:
        icon = 6361
        color = "#f4ea1f"
    elif SOC <= 81:
        icon = 6362
        color = "#b6e61a"
    elif SOC <= 99:
        icon = 6363
        color = "#2cf046"
    
    #Aufbereitung der Daten für die Anzeige in der App
    data_app = {
        "text": str(SOC) + " %",
        "progress": SOC,
        "progressc": "#00ff00",
        "icon": icon,
        "color": color,
    }
    # Senden der Daten an Awtrix3
    awtrix3_send_app(
        config["awtrix3"]["url"],
        app,
        data_app,
        config["settings"]["app_scroll_duration"],
        config["settings"]["app_show_time"],
    )
